import os
from typing import Type, TypeVar
from openai import OpenAI
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')

    def text(self, system: str, user: str, temperature: float = 0.2) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
        )
        return response.choices[0].message.content or ''

    def structured(self, system: str, user: str, schema: Type[T]) -> T:
        response = self.client.chat.completions.parse(
            model=self.model,
            temperature=0.2,
            messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
            response_format=schema,
        )
        return response.choices[0].message.parsed
