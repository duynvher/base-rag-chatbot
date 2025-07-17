from fastapi import APIRouter

from src.memory.thread_history import ThreadHistory

router = APIRouter()
thread_history = ThreadHistory()


@router.get("/v1/audit/{chat_id:path}")
async def get_audit(chat_id: str):
    return await thread_history.get_conversation(thread_id=chat_id)
