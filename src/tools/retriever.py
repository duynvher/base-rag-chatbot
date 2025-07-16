import asyncio

from langchain.tools import BaseTool

from src.knowledge import knowledge_base


class Retriever(BaseTool):
    name: str = "retriever"
    description: str = "Retrieves information in knowledge base using to answer questions."

    async def _arun(self, query: str) -> str:
        documents = await knowledge_base.vector_store.asimilarity_search(query=query, k=1)
        contents = [doc.page_content for doc in documents]

        return "\n".join(contents)

    def _run(self, query: str) -> str:
        """Fallback sync version"""
        return asyncio.run(self._arun(query))
