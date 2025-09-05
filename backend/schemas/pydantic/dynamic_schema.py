import enum

from typing import Optional, List
from pydantic import BaseModel, Field


class EmploymentTypeEnum(str, enum.Enum):
    """Case-insensitive Enum for employment types."""

    @classmethod
    def _missing_(cls, value: object):
        """Handles case-insensitive lookup."""
        if isinstance(value, str):
            value_lower = value.lower()
            mapping = {member.value.lower(): member for member in cls}
            if value_lower in mapping:
                return mapping[value_lower]

        raise ValueError()


class RemoteStatusEnum(str, enum.Enum):
    @classmethod
    def _missing_(cls, value: object):
        """Handles case-insensitive lookup."""
        if isinstance(value, str):
            value_lower = value.lower()
            mapping = {member.value.lower(): member for member in cls}
            if value_lower in mapping:
                return mapping[value_lower]

        raise ValueError()


class CompanyProfile(BaseModel):
    company_name: str = Field(..., alias="companyName")
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class Effective_date(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    remote_status: RemoteStatusEnum = Field(..., alias="remoteStatus")


class Qualifications(BaseModel):
    required: List[str]
    preferred: Optional[List[str]] = None


class CompensationAndBenefits(BaseModel):
    salary_range: Optional[str] = Field(..., alias="salaryRange")
    benefits: Optional[List[str]] = None

class StructuredmodelModel(BaseModel):
    model_title: str = Field(..., alias="modelTitle")
    company_profile: CompanyProfile = Field(..., alias="companyProfile")
    effective_date: effective_date
    date_posted: str = Field(..., alias="datePosted")
    employment_type: EmploymentTypeEnum = Field(..., alias="employmentType")
    model_summary: str = Field(..., alias="modelSummary")
    key_responsibilities: List[str] = Field(..., alias="keyResponsibilities")
    qualifications: Qualifications
    compensation_and_benefits: Optional[CompensationAndBenefits] = Field(
        None, alias="compensationAndBenefits"
    )
    application_info: Optional[ApplicationInfo] = Field(None, alias="applicationInfo")
    extracted_keywords: List[str] = Field(..., alias="extractedKeywords")

    class ConfigDict:
        validate_by_name = True
        str_strip_whitespace = True
