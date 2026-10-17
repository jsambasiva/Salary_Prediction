from typing import Literal

from pydantic import BaseModel, Field


class SalaryRequest(BaseModel):
    experience: float = Field(..., ge=0, le=40, description="Years of experience")
    education: Literal["High School", "Bachelor", "Master", "PhD"]
    job_role: Literal[
        "Software Engineer",
        "Data Scientist",
        "Data Analyst",
        "Web Developer",
        "DevOps Engineer",
        "UI/UX Designer",
    ]
    city_tier: Literal["Tier 1", "Tier 2", "Tier 3"]


class SalaryResponse(BaseModel):
    predicted_salary: float
    lower_estimate: float
    upper_estimate: float
    currency: str = "INR"
