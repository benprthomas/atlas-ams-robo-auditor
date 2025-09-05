from uuid import UUID
from typing import List
from pydantic import BaseModel, Field


class modelUploadRequest(BaseModel):
    model_descriptions: List[str] = Field(
        ..., description="List of model descriptions in markdown format"
    )
    cur_id: UUID = Field(..., description="UUID reference to the cur")
