import os
from pydantic import BaseModel, Field
import httpx
import json

class Client(BaseModel):
    api_base: str = Field(default_factory=lambda: os.getenv("CHATBOT_API_BASE", "http://localhost:6868"))

    async def call(self, query: str, thread_id: str, user_id: str):
        endpoint = f"{self.api_base}/v1/chat"
        payload = {
            "query": query,
            "thread_id": thread_id,
            "user_id": user_id,
        }

        async with httpx.AsyncClient() as client:
            async with client.stream("POST", endpoint, json=payload) as response:
                async for line in response.aiter_text():
                    yield json.loads(line)

