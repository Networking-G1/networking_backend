# routers/extra.py
from select import select
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from crud import create_skill, add_skill_to_user, get_user, get_user_skills, create_job_application, get_applications_for_user, send_message, get_conversation_messages, create_conversation, add_admin_monitor
from models.extra import ActivityLog, JobApplication, JobApplicationStatus, Message
from schemas.extra import SkillCreate, JobApplicationCreate, MessageCreate
from deps import get_current_user
from sqlalchemy import desc
router = APIRouter()

# Skills
@router.post("/skills", status_code=201)
def create_skill_route(payload: SkillCreate, session: Session = Depends(get_session)):
    return create_skill(session, name=payload.name, type=payload.type)

@router.post("/users/{user_id}/skills", status_code=201)
def add_skill(user_id: int, payload: SkillCreate, session: Session = Depends(get_session)):
    # ensure user exists
    skill = create_skill(session, name=payload.name, type=payload.type)
    # assign
    return add_skill_to_user(session, get_user(session, user_id), skill, level=1)

@router.get("/skills/{user_id}")
def get_user_skills_route(user_id: int, session: Session = Depends(get_session)):
    user = get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # retorna la estructura limpia
    return [
        {
            "id": us.skill.id,
            "name": us.skill.name,
            "type": us.skill.type,
            "level": us.level
        }
        for us in user.skills
    ]

# Job applications
@router.post("/users/{user_id}/applications", status_code=201)
def apply_job(user_id: int, payload: JobApplicationCreate, session: Session = Depends(get_session)):
    # you can verify job exists in external backend optionally
    return create_job_application(session, user_id=user_id, job_id=payload.job_id)

@router.get("/users/{user_id}/applications")
def list_applications(user_id: int, session: Session = Depends(get_session)):
    return get_applications_for_user(session, user_id)

# Messaging
@router.post("/conversations", status_code=201)
def create_conv(session: Session = Depends(get_session)):
    return create_conversation(session)

@router.post("/messages", status_code=201)
def post_message(payload: MessageCreate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    return send_message(session, payload.conversation_id, current_user.id, payload.content)

@router.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int, session: Session = Depends(get_session)):
    return get_conversation_messages(session, conversation_id)

# Admin monitor
@router.post("/admin/monitor", status_code=201)
def monitor_user(payload: dict, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    person_id = payload.get("person_id")
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    return add_admin_monitor(session, current_user.id, person_id)

@router.get("/admin/user-report/{user_id}")
def user_report(user_id: int, session: Session = Depends(get_session), current_user = Depends(get_current_user)):
    # permissions
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    # skills
    skills = get_user_skills(session, user_id)
    # applications
    stmt = select(JobApplication).where(JobApplication.user_id == user_id)
    apps = session.exec(stmt).all()
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    day_count = sum(1 for a in apps if a.created_at >= day_ago)
    week_count = sum(1 for a in apps if a.created_at >= week_ago)
    month_count = sum(1 for a in apps if a.created_at >= month_ago)
    hired = any(a.status == JobApplicationStatus.hired for a in apps)
    # activities
    
    activities = session.exec(select(ActivityLog).where(ActivityLog.user_id == user_id).order_by(desc(ActivityLog.created_at)).limit(20)).all()
    # messages count
    messages_count = session.exec(select(Message).where(Message.sender_id == user_id)).count()
    return {
        "skills": [ {"skill_id": s.skill_id, "level": s.level, "endorsements": s.endorsements} for s in skills],
        "applications": {"day": day_count, "week": week_count, "month": month_count},
        "hired": hired,
        "activities": [ {"type": act.type, "metadata": act.metadata, "created_at": act.created_at} for act in activities],
        "messages_sent": messages_count
    }
