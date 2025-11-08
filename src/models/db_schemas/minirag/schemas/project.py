from .minirag_base import SQLAlchamyBase
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

class Project(SQLAlchamyBase):

    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True , nullable=True)
    assets = relationship("Asset", back_populates="project")
    chunks = relationship("Chunk", back_populates="project")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable= False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable= True)
