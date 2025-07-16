from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.agents.agent import GeneralAgent

agent = GeneralAgent()

router = APIRouter()


@router.post("/v1/chat")
async def chat(query: str, thread_id: str, user_id: str):
    response = agent.astream(user_query=query, thread_id=thread_id, user_id=user_id)

    return StreamingResponse(response, media_type="text/plain")
