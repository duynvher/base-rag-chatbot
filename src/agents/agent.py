import json

from langchain_core.runnables.config import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from src.memory.memory_saver import PGMemorySaver
from src.tools.retriever import Retriever


class GeneralAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0,
            thinking_budget=0,
        )

        self.tools = [Retriever()]

    async def astream(self, user_query: str, thread_id: str, user_id: str = None):
        async with PGMemorySaver().get_checkpointer() as checkpointer:
            graph = create_react_agent(self.llm, tools=self.tools, checkpointer=checkpointer)
            config = RunnableConfig(configurable={"thread_id": thread_id, "user_id": user_id})
            response = graph.astream_events(
                {"messages": [{"role": "user", "content": user_query}]}, config
            )

            async for chunk in response:
                if chunk["event"] == "on_chat_model_stream":
                    data = chunk["data"]["chunk"]
                    yield json.dumps({"id": data.id, "content": data.content}, ensure_ascii=False)
