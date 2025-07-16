from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.agents.agent import GeneralAgent
from src.models import ChatRequest

agent = GeneralAgent()

router = APIRouter()


@router.post("/v1/chat")
async def chat(request: ChatRequest):
    response = agent.astream(
        user_query=request.query, thread_id=request.thread_id, user_id=request.user_id
    )

    return StreamingResponse(response, media_type="text/plain")
