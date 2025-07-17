import asyncio

from langchain.tools import BaseTool

from src.knowledge import knowledge_base


class Retriever(BaseTool):
    name: str = "retriever"
    description: str = (
        "A tool that searches a knowledge base "
        "and returns relevant documents based on the user’s query. "
        "Use this tool when the question may require specific factual "
        "or contextual information that might be found in stored documents "
        "(e.g., internal documents, FAQs, manuals, articles)."
    )

    async def _arun(self, query: str) -> str:
        documents = await knowledge_base.vector_store.asimilarity_search(query=query, k=3)
        contents = [doc.page_content for doc in documents]

        return "\n".join(contents)

    def _run(self, query: str) -> str:
        """Fallback sync version"""
        return asyncio.run(self._arun(query))
