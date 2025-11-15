from .BaseDataModel import BaseDataModel
from .db_schemas import DataChunk
from .enums.data_base_enums import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import delete
from bson.objectid import ObjectId


class ChunkModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """Factory method for async initialization."""
        instance = cls(db_client)
        return instance

    async def create_chunk(self, chunk: DataChunk):
        """Insert a single DataChunk record."""
        async with self.db_client() as session:
            session.add(chunk)
            await session.commit()
            await session.refresh(chunk)
        return chunk

    async def get_chunk(self, chunk_id: str):
        """Retrieve a single DataChunk by its ID."""
        async with self.db_client() as session:
            stmt = select(DataChunk).where(DataChunk.id == chunk_id)
            result = await session.execute(stmt)
            chunk = result.scalar_one_or_none()
        return chunk

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        """Insert multiple DataChunk records in batches."""
        async with self.db_client() as session:
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                session.add_all(batch)
                await session.commit()
        return len(chunks)

    async def delete_chunk_by_project_id(self, project_id: ObjectId):
        """Delete all chunks belonging to a given project."""
        async with self.db_client() as session:
            result = await session.execute(
                delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
            )
            await session.commit()
        return result.rowcount

    async def get_project_chunks(self, project_id: ObjectId, page_no: int = 1, page_size: int = 50):
        """Paginate chunks for a given project."""
        async with self.db_client() as session:
            stmt = (
                select(DataChunk)
                .where(DataChunk.chunk_project_id == project_id)
                .offset((page_no - 1) * page_size)
                .limit(page_size)
            )
            result = await session.execute(stmt)
            records = result.scalars().all()
        return records
