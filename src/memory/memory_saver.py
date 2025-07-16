import os
from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel, Field, model_validator


class PGMemorySaver(BaseModel):
    pg_connection_string: str = Field(default_factory=lambda: os.getenv("PG_CONNECTION"))

    @model_validator(mode="after")
    def setup(self):
        assert self.pg_connection_string, "PG_CONNECTION environment variable not set."
        self.pg_connection_string = self.pg_connection_string.replace("+psycopg", "")
        return self

    @asynccontextmanager
    async def get_checkpointer(self):
        """
        Context manager that provides an AsyncPostgresSaver instance.
        Handles connection pool creation and cleanup.
        """
        async with AsyncConnectionPool(
            conninfo=self.pg_connection_string,
            max_size=20,
        ) as pool, pool.connection() as conn:
            checkpointer = AsyncPostgresSaver(conn)
            yield checkpointer
