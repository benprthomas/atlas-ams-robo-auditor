from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentData(BaseModel):
    firstName: str = Field(..., alias="firstName")
    lastName: Optional[str] = Field(..., alias="lastName")
    company: str
    hoc: str
    adoption: Optional[str] = None
    portfolio: Optional[str] = None
    effective_date: effective_date


class Experience(BaseModel):
    model_title: str = Field(..., alias="modelTitle")
    company: str
    effective_date: str
    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    description: List[str]
    technologies_used: Optional[List[str]] = Field(
        default_factory=list, alias=""
    )


class amendment(BaseModel):
    category: str
    amendment_name: str = Field(..., alias="amendmentName")

class StructuredcurModel(BaseModel):
    personal_data: PersonalData = Field(..., alias="Personal Data")
    experiences: List[Experience] = Field(..., alias="Experiences")
    amendments: List[amendment] = Field(..., alias="amendments")
    provision: List[provision] = Field(..., alias="provision")
    extracted_keywords: List[str] = Field(
        default_factory=list, alias="Extracted Keywords"
    )

    class ConfigDict:
        validate_by_name = True
        str_strip_whitespace = True
