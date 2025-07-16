from fastapi import APIRouter
from langchain_core.runnables.config import RunnableConfig

from src.memory.memory_saver import PGMemorySaver

router = APIRouter()


@router.get("/v1/audit/{chat_id:path}")
async def get_audit(chat_id: str):
    async with PGMemorySaver().get_checkpointer() as checkpointer:
        return await checkpointer.aget(RunnableConfig(configurable={"thread_id": chat_id}))
