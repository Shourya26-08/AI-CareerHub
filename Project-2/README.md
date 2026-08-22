# Project 2 — Dispatch Mini Social Media Platform

A full-stack social media application built with **Django + Django REST Framework** and a lightweight HTML/CSS/JavaScript frontend.

## Features
- User registration, login and logout
- Token-based authentication
- User profiles with bio and avatar URL
- Global and following feeds
- Create and delete posts
- Like/unlike posts
- Comments API
- Follow/unfollow users
- Followers/following endpoints
- Django admin

## Run the backend
```bash
cd backend
python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API: `http://127.0.0.1:8000/api/`

## Run the frontend
In another terminal:
```bash
cd frontend
python -m http.server 5500
```
Open `http://127.0.0.1:5500`.

## Internship project
**Project 2 — Mini Social Media Platform**
