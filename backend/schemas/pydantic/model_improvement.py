from uuid import UUID
from pydantic import BaseModel, Field


class curImprovementRequest(BaseModel):
    model_id: UUID = Field(..., description="DB UUID reference to the model")
    cur_id: UUID = Field(..., description="DB UUID reference to the cur")
