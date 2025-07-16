import json

from langchain_core.runnables.config import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from src.memory import memory
from src.tools.retriever import Retriever


class GeneralAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0,
            thinking_budget=0,
        )

        self.tools = [Retriever()]

        self.memory = memory

        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=(
                "You are a helpful assistant. "
                "First, you need to use the retriever tool to get information. "
                "Then use the retriever's information to answer the user's question. "
                "If the information cannot be used to answer, say, 'I don't know.'"
            ),
            checkpointer=self.memory,
        )

    async def astream(self, user_query: str, thread_id: str, user_id: str = None):
        config = RunnableConfig(configurable={"thread_id": thread_id, "user_id": user_id})
        response = self.agent.astream_events(
            {"messages": [{"role": "user", "content": user_query}]}, config
        )

        async for chunk in response:
            if chunk["event"] == "on_chat_model_stream":
                data = chunk["data"]["chunk"]
                yield json.dumps({"id": data.id, "content": data.content}, ensure_ascii=False)
