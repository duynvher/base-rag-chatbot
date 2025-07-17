from typing import List

from fastapi import APIRouter, File, UploadFile

from src.knowledge import knowledge_base
from src.models import UpdateKnowledgeInput, UpdateKnowledgeOutput

router = APIRouter()


@router.post("/v1/knowledge/update/texts", response_model=List[UpdateKnowledgeOutput])
async def update_knowledge(request: UpdateKnowledgeInput):
    documents = await knowledge_base.add_document(documents=request.documents)
    return documents


@router.post("/v1/knowledge/update/documents")
async def update_knowledge(files: List[UploadFile] = File(...)):
    return "Upcoming feature"


@router.delete("/v1/knowledge/{document_id:path}")
async def delete_knowledge(document_id: str):
    await knowledge_base.del_document(document_id=document_id)
    return {"status": "success"}


@router.get("/v1/knowledge")
async def get_knowledge():
    documents = await knowledge_base.get_all_documents()
    return documents
