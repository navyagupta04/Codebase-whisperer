from typing import Literal

from pydantic import BaseModel


class DeveloperProfile(BaseModel):
    role: Literal["backend", "frontend", "devops", "docs"] = "backend"
    skill_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    language: str = "English"
    hours_per_week: int = 5
    goal: str = "fix a bug"
