from typing import List

from pydantic import BaseModel


class UpdateKnowledgeInput(BaseModel):
    documents: List[str]


class UpdateKnowledgeOutput(BaseModel):
    id: str
    page_content: str
