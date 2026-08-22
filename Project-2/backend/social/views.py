from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics,status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post,Comment,Like,Follow
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer,ProfileUpdateSerializer,PostSerializer,PostDetailSerializer,CommentSerializer,FollowUserSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj): return request.method in permissions.SAFE_METHODS or obj.author==request.user

class RegisterView(generics.CreateAPIView):
    permission_classes=[permissions.AllowAny]; serializer_class=RegisterSerializer
    def create(self,request,*args,**kwargs):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); user=s.save(); token,_=Token.objects.get_or_create(user=user)
        return Response({'token':token.key,'username':user.username},status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        s=LoginSerializer(data=request.data); s.is_valid(raise_exception=True); user=authenticate(username=s.validated_data['username'],password=s.validated_data['password'])
        if user is None:return Response({'detail':'Invalid username or password.'},status=status.HTTP_401_UNAUTHORIZED)
        token,_=Token.objects.get_or_create(user=user); return Response({'token':token.key,'username':user.username})

class LogoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request): request.user.auth_token.delete(); return Response(status=status.HTTP_204_NO_CONTENT)

class MeView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request): return Response(ProfileSerializer(request.user.profile,context={'request':request}).data)

class ProfileDetailView(APIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get(self,request,username): return Response(ProfileSerializer(get_object_or_404(User,username__iexact=username).profile,context={'request':request}).data)

class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]; serializer_class=ProfileUpdateSerializer
    def get_object(self): return self.request.user.profile
    def update(self,request,*args,**kwargs):
        super().update(request,*args,**kwargs); return Response(ProfileSerializer(self.request.user.profile,context={'request':request}).data)

class FeedView(generics.ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]; serializer_class=PostSerializer
    def get_queryset(self):
        qs=Post.objects.select_related('author','author__profile')
        if self.request.query_params.get('feed')=='following' and self.request.user.is_authenticated:
            ids=Follow.objects.filter(follower=self.request.user).values_list('following_id',flat=True); qs=qs.filter(author_id__in=ids)
        return qs
    def perform_create(self,serializer): serializer.save(author=self.request.user)
    def get_serializer_context(self): return {'request':self.request}

class PostDetailView(generics.RetrieveDestroyAPIView):
    queryset=Post.objects.all(); serializer_class=PostDetailSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]
    def get_serializer_context(self): return {'request':self.request}

class UserPostsView(generics.ListAPIView):
    serializer_class=PostSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self): return Post.objects.filter(author__username__iexact=self.kwargs['username'])
    def get_serializer_context(self): return {'request':self.request}

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class=CommentSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self): return Comment.objects.filter(post_id=self.kwargs['post_id'])
    def perform_create(self,serializer): serializer.save(author=self.request.user,post=get_object_or_404(Post,pk=self.kwargs['post_id']))

class CommentDeleteView(generics.DestroyAPIView):
    queryset=Comment.objects.all(); serializer_class=CommentSerializer; permission_classes=[permissions.IsAuthenticated,IsAuthorOrReadOnly]

class LikeToggleView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,post_id):
        post=get_object_or_404(Post,pk=post_id); _,created=Like.objects.get_or_create(post=post,user=request.user); return Response({'liked':True,'likes_count':post.likes.count()},status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    def delete(self,request,post_id):
        post=get_object_or_404(Post,pk=post_id); Like.objects.filter(post=post,user=request.user).delete(); return Response({'liked':False,'likes_count':post.likes.count()})

class FollowToggleView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,username):
        target=get_object_or_404(User,username__iexact=username)
        if target==request.user:return Response({'detail':"You can't follow yourself."},status=400)
        _,created=Follow.objects.get_or_create(follower=request.user,following=target); return Response({'following':True,'followers_count':Follow.objects.filter(following=target).count()},status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    def delete(self,request,username):
        target=get_object_or_404(User,username__iexact=username); Follow.objects.filter(follower=request.user,following=target).delete(); return Response({'following':False,'followers_count':Follow.objects.filter(following=target).count()})

class FollowersListView(generics.ListAPIView):
    serializer_class=FollowUserSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        user=get_object_or_404(User,username__iexact=self.kwargs['username']); return Follow.objects.filter(following=user).select_related('follower__profile')
    def get_serializer(self,*args,**kwargs):
        qs=args[0] if args else self.get_queryset(); wrapped=[type('Row',(),{'user':f.follower})() for f in qs]; return super().get_serializer(wrapped,many=True,**kwargs)

class FollowingListView(generics.ListAPIView):
    serializer_class=FollowUserSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        user=get_object_or_404(User,username__iexact=self.kwargs['username']); return Follow.objects.filter(follower=user).select_related('following__profile')
    def get_serializer(self,*args,**kwargs):
        qs=args[0] if args else self.get_queryset(); wrapped=[type('Row',(),{'user':f.following})() for f in qs]; return super().get_serializer(wrapped,many=True,**kwargs)
