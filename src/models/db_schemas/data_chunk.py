from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId]
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict 
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId


    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value
    
    class Config:
        arbitrary_types_allowed = True