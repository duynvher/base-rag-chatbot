from fastapi import FastAPI

from .endpoints.audit import router as audit_router
from .endpoints.chat import router as chat_router
from .endpoints.knowledge import router as knowledge_router

app = FastAPI()


@app.get("/health", tags=["health"])
async def health():
    return 200


app.include_router(chat_router, tags=["chat"])
app.include_router(knowledge_router, tags=["knowledge"])
app.include_router(audit_router, tags=["audit"])
