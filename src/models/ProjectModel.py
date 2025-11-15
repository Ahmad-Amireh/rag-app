from .BaseDataModel import BaseDataModel
from .db_schemas import Project
from .enums.data_base_enums import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func
import math


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """Factory method for async initialization."""
        instance = cls(db_client)
        return instance

    async def create_project(self, project: Project):
        """Insert a new project record."""
        async with self.db_client() as session:
            session.add(project)
            await session.commit()
            await session.refresh(project)
        return project

    async def get_project_or_create_one(self, project_id: str):
        """Fetch a project by ID, or create it if it doesn’t exist."""
        async with self.db_client() as session:
            stmt = select(Project).where(Project.project_id == project_id)
            result = await session.execute(stmt)
            project = result.scalar_one_or_none()

            if project is None:
                project = Project(project_id=project_id)
                project = await self.create_project(project)

            return project

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """Paginated list of all projects."""
        async with self.db_client() as session:
            total_query = select(func.count(Project.project_id))
            total_result = await session.execute(total_query)
            total_documents = total_result.scalar_one()

            total_pages = math.ceil(total_documents / page_size) if total_documents else 1

            stmt = (
                select(Project)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            result = await session.execute(stmt)
            projects = result.scalars().all()

        return projects, total_pages
