from fastapi import APIRouter
from langchain_core.runnables.config import RunnableConfig

from src.memory import memory

router = APIRouter()


@router.get("/v1/audit/{chat_id:path}")
async def get_audit(chat_id: str):
    config = RunnableConfig(configurable={"thread_id": chat_id})
    return memory.get_tuple(config)[1]["channel_values"]["messages"]
