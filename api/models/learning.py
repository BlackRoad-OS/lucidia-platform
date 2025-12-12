"""Learning plan models for personalized study schedules."""
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class StudyPlanRequest(BaseModel):
    """Incoming request to generate a study plan."""

    subject: str = Field(..., description="Primary subject for the plan (e.g. math, physics)")
    target_competency: str = Field(
        ..., description="What the learner hopes to achieve by the end of the plan"
    )
    topics: List[str] = Field(..., description="Key topics to focus on during the plan")
    days: int = Field(5, ge=1, le=30, description="Number of study days to schedule")
    daily_time_minutes: int = Field(
        45, ge=15, le=240, description="Available time per day for studying"
    )
    start_date: Optional[date] = Field(None, description="Optional custom start date")


class Lesson(BaseModel):
    """A focused learning task inside a study session."""

    title: str
    focus: str
    duration_minutes: int
    resources: List[str] = Field(default_factory=list)
    practice_prompt: Optional[str] = None
    reflection_question: Optional[str] = None


class StudySession(BaseModel):
    """A single scheduled study session."""

    day: int
    date: date
    focus: str
    lessons: List[Lesson]
    retention_activity: str
    checkpoint_question: str


class StudyPlan(BaseModel):
    """Generated study plan with scheduled sessions."""

    id: str
    subject: str
    target_competency: str
    topics: List[str]
    daily_time_minutes: int
    sessions: List[StudySession]
    created_at: datetime


class ProgressUpdate(BaseModel):
    """Request to record progress on a study session."""

    session_day: int = Field(..., ge=1, description="Day number being completed")
    notes: Optional[str] = Field(None, description="Optional learner notes")
    confidence: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Learner self-assessed confidence (1-5)",
    )


class PlanProgress(BaseModel):
    """Progress tracking for a study plan."""

    plan_id: str
    completed_sessions: List[int]
    notes: List[str] = Field(default_factory=list)
    average_confidence: Optional[float] = None
    next_session_hint: Optional[str] = None
