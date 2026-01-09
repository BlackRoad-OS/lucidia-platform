"""Learning plan endpoints for structured study schedules."""
from datetime import datetime, timedelta
from typing import Dict, List
import uuid

from fastapi import APIRouter, HTTPException

from models.learning import (
    StudyPlanRequest,
    StudyPlan,
    StudySession,
    Lesson,
    PlanProgress,
    ProgressUpdate,
)

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])

learning_plans: Dict[str, StudyPlan] = {}
plan_progress: Dict[str, PlanProgress] = {}


@router.post("/plan", response_model=StudyPlan)
async def create_study_plan(request: StudyPlanRequest) -> StudyPlan:
    """Generate a study plan based on learner goals and availability."""
    plan_id = str(uuid.uuid4())
    start_date = request.start_date or datetime.utcnow().date()
    sessions: List[StudySession] = []

    for day in range(request.days):
        session_date = start_date + timedelta(days=day)
        focus_topic = request.topics[day % len(request.topics)]

        lessons = _build_lessons_for_topic(
            focus_topic,
            request.subject,
            request.daily_time_minutes,
        )

        sessions.append(
            StudySession(
                day=day + 1,
                date=session_date,
                focus=focus_topic,
                lessons=lessons,
                retention_activity=f"Create a 5-minute summary of today's {request.subject} topic",
                checkpoint_question=f"What is the one thing about {focus_topic} you can teach back?",
            )
        )

    plan = StudyPlan(
        id=plan_id,
        subject=request.subject,
        target_competency=request.target_competency,
        topics=request.topics,
        daily_time_minutes=request.daily_time_minutes,
        sessions=sessions,
        created_at=datetime.utcnow(),
    )

    learning_plans[plan_id] = plan
    plan_progress[plan_id] = PlanProgress(
        plan_id=plan_id,
        completed_sessions=[],
        notes=[],
        average_confidence=None,
        next_session_hint="Start with a quick recap before beginning the next session",
    )

    return plan


@router.get("/plan/{plan_id}", response_model=StudyPlan)
async def get_study_plan(plan_id: str) -> StudyPlan:
    """Retrieve a previously generated study plan."""
    plan = learning_plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Study plan not found")
    return plan


@router.get("/plan/{plan_id}/progress", response_model=PlanProgress)
async def get_plan_progress(plan_id: str) -> PlanProgress:
    """Get progress information for a study plan."""
    progress = plan_progress.get(plan_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Plan progress not found")
    return progress


@router.post("/plan/{plan_id}/progress", response_model=PlanProgress)
async def update_plan_progress(plan_id: str, update: ProgressUpdate) -> PlanProgress:
    """Mark a study session as completed with optional notes and confidence."""
    if plan_id not in learning_plans:
        raise HTTPException(status_code=404, detail="Study plan not found")

    progress = plan_progress.get(plan_id)
    if not progress:
        progress = PlanProgress(
            plan_id=plan_id, completed_sessions=[], notes=[], average_confidence=None
        )
        plan_progress[plan_id] = progress

    if update.session_day not in progress.completed_sessions:
        progress.completed_sessions.append(update.session_day)

    if update.notes:
        progress.notes.append(update.notes)

    if update.confidence is not None:
        _update_average_confidence(progress, update.confidence)

    progress.next_session_hint = _build_next_hint(
        learning_plans[plan_id], progress
    )

    return progress


def _build_lessons_for_topic(
    topic: str,
    subject: str,
    daily_time: int,
) -> List[Lesson]:
    """Create a set of lessons that fits within the daily time budget."""
    base_duration = max(15, daily_time // 3)
    practice_duration = max(10, daily_time // 4)
    review_duration = max(10, daily_time - base_duration - practice_duration)

    return [
        Lesson(
            title="Concept Overview",
            focus=f"Why {topic} matters in {subject}",
            duration_minutes=base_duration,
            resources=[
                f"Short article on {topic}",
                f"2-minute visual explainer: {topic}",
            ],
            reflection_question=f"Where have you seen {topic} used before?",
        ),
        Lesson(
            title="Guided Practice",
            focus=f"Work through core examples for {topic}",
            duration_minutes=practice_duration,
            resources=["Interactive practice set", "Hinted problem walkthrough"],
            practice_prompt=f"Solve two problems that apply {topic} in context",
        ),
        Lesson(
            title="Active Recall",
            focus=f"Summarize the most important ideas about {topic}",
            duration_minutes=review_duration,
            resources=["Flashcard prompts", "Self-quiz checklist"],
            reflection_question=f"Explain {topic} to a friend in one minute",
        ),
    ]


def _update_average_confidence(progress: PlanProgress, confidence: int) -> None:
    """Update rolling average confidence as new ratings arrive."""
    total_entries = len(progress.completed_sessions)
    if progress.average_confidence is None:
        progress.average_confidence = confidence
        return

    progress.average_confidence = round(
        ((progress.average_confidence * (total_entries - 1)) + confidence)
        / total_entries,
        2,
    )


def _build_next_hint(plan: StudyPlan, progress: PlanProgress) -> str:
    """Provide a short hint for the next session."""
    remaining_sessions = [
        session for session in plan.sessions if session.day not in progress.completed_sessions
    ]
    if not remaining_sessions:
        return "Plan complete! Create a new plan or revisit tough topics."

    next_session = remaining_sessions[0]
    return (
        f"Next up: {next_session.focus} on {next_session.date}."
        " Start with a 3-minute recap before diving in."
    )
