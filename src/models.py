from typing import List, Optional

from pydantic import BaseModel


class UpdateKnowledgeInput(BaseModel):
    documents: List[str]


class UpdateKnowledgeOutput(BaseModel):
    id: str
    page_content: str


class ChatRequest(BaseModel):
    query: str
    thread_id: str
    user_id: Optional[str] = None
