import json
import os
import uuid
from typing import List, Optional

import asyncpg
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import select

from src.models import UpdateKnowledgeOutput


class KnowledgeBase(BaseModel):
    pg_connection: Optional[str] = Field(default_factory=lambda: os.getenv("PG_CONNECTION", None))
    pg_collection: str = Field(default_factory=lambda: os.getenv("PG_COLLECTION_NAME", "default"))

    vector_store: PGVector = None

    embedding_model: str = Field(
        default_factory=lambda: os.getenv("EMBEDDING_MODEL", "models/embedding-001")
    )

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def validate_env(self):
        assert self.pg_connection, "PG_CONNECTION is not set."
        return self

    @model_validator(mode="after")
    def setup(self):
        embeddings = GoogleGenerativeAIEmbeddings(model=self.embedding_model)

        self.vector_store = PGVector(
            embeddings=embeddings,
            collection_name=self.pg_collection,
            connection=self.pg_connection,
            use_jsonb=True,
            async_mode=True,
        )
        return self

    async def add_document(self, documents: List[str]):
        documents = [
            Document(
                page_content=content,
                metadata={"id": uuid.uuid4().hex},
            )
            for content in documents
        ]
        await self.vector_store.aadd_documents(
            documents, ids=[doc.metadata["id"] for doc in documents]
        )
        return [
            UpdateKnowledgeOutput(id=doc.metadata.get("id"), page_content=doc.page_content)
            for doc in documents
        ]

    async def del_document(self, document_id: str):
        await self.vector_store.adelete([document_id])

    async def get_documents(self):
        conn = await asyncpg.connect(self.pg_connection.replace("+psycopg", ""))
        rows = await conn.fetch(
            """
            SELECT e.document AS page_content, e.cmetadata AS metadata
            FROM langchain_pg_embedding AS e
                     JOIN langchain_pg_collection AS c
                          ON e.collection_id = c.uuid
            WHERE c.name = $1
            """,
            self.pg_collection,
        )
        await conn.close()

        return [
            Document(page_content=r["page_content"], metadata=json.loads(r["metadata"]))
            for r in rows
        ]

    async def get_all_documents(self):
        async with self.vector_store._make_async_session() as session:
            # Retrieve the collection object inside PGVector
            collection = await self.vector_store.aget_collection(session)

            if not collection:
                self.logger.warning("Collection not found")
                return []

            stmt = select(
                self.vector_store.EmbeddingStore.document,
                self.vector_store.EmbeddingStore.cmetadata,
            ).where(self.vector_store.EmbeddingStore.collection_id == collection.uuid)

            result = await session.execute(stmt)
            rows = result.all()

        documents = [
            UpdateKnowledgeOutput(id=metadata.get("id"), page_content=content)
            for content, metadata in rows
        ]
        return documents
