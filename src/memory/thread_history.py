import copy

from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel

from src.memory.memory_saver import PGMemorySaver
from src.models import ConversationData


class ThreadHistory(BaseModel):
    async def get_thread_data(self, thread_id: str):
        async with PGMemorySaver().get_checkpointer() as checkpointer:
            data = await checkpointer.aget(
                RunnableConfig(configurable={"thread_id": thread_id})
            )

        messages = data["channel_values"]["messages"]
        return self.convert_chat_to_pairs(messages)

    @staticmethod
    def convert_chat_to_pairs(chat_data):
        pairs = []
        pair = ConversationData()

        for message in chat_data:
            if message.type == "human":
                pair.query = message.content
            elif message.type == "tool":
                pair.tool_content = message.content
            elif message.type == "ai" and message.content:
                pair.response = message.content
                pairs.append(copy.deepcopy(pair))
                pair = ConversationData()

        return pairs
