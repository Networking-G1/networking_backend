# crud.py
from sqlmodel import Session, select
from models.user import User
from auth import hash_password, verify_password
from typing import Optional, List
from models.extra import Skill, UserSkill, Hobby, UserHobby, Preference, ActivityLog, JobApplication, AdminMonitor, Conversation, Message
from datetime import datetime
from models.profile import AboutMe, WorkExperience, Education

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def create_user(session: Session, email: str, password: str, full_name: str | None = None, role = None) -> User:
    hashed = hash_password(password)
    user = User(email=email, hashed_password=hashed, full_name=full_name, role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def set_password(session: Session, user: User, new_password: str):
    user.hashed_password = hash_password(new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# SKILLS
def create_skill(session: Session, name: str, type: str = "hard") -> Skill:
    skill = Skill(name=name, type=type)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

def add_skill_to_user(session: Session, user: User, skill: Skill, level: int = 1) -> UserSkill:
    us = UserSkill(user_id=user.id, skill_id=skill.id, level=level)
    session.add(us)
    session.commit()
    session.refresh(us)
    return us

def get_user_skills(session: Session, user_id: int) -> List[UserSkill]:
    stmt = select(UserSkill).where(UserSkill.user_id == user_id)
    return session.exec(stmt).all()

# HOBBIES / PREFERENCES similar pattern
def add_activity(session: Session, user_id: int, type: str, details: str | None = None):
    act = ActivityLog(user_id=user_id, type=type, details=details)
    session.add(act)
    session.commit()
    session.refresh(act)
    return act


# JOB APPLICATIONS
def create_job_application(session: Session, user_id: int, job_id: int) -> JobApplication:
    app = JobApplication(user_id=user_id, job_id=job_id, status="applied", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    session.add(app)
    session.commit()
    session.refresh(app)
    return app

def update_job_application_status(session: Session, application_id: int, status: str):
    app = session.get(JobApplication, application_id)
    if not app:
        return None
    app.status = status
    app.updated_at = datetime.utcnow()
    session.add(app)
    session.commit()
    session.refresh(app)
    return app

def get_applications_for_user(session: Session, user_id: int):
    stmt = select(JobApplication).where(JobApplication.user_id == user_id)
    return session.exec(stmt).all()

# MESSAGING
def create_conversation(session: Session, title: str | None = None) -> Conversation:
    conv = Conversation(title=title)
    session.add(conv)
    session.commit()
    session.refresh(conv)
    return conv

def send_message(session: Session, conversation_id: int, sender_id: int, content: str) -> Message:
    msg = Message(conversation_id=conversation_id, sender_id=sender_id, content=content)
    session.add(msg)
    session.commit()
    session.refresh(msg)
    # add activity log
    add_activity(session, sender_id, "message_sent", details=str({"conversation_id": conversation_id}))
    return msg

def get_conversation_messages(session: Session, conversation_id: int):
    stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    return session.exec(stmt).all()

# ADMIN MONITOR
def add_admin_monitor(session: Session, admin_id: int, person_id: int):
    entry = AdminMonitor(admin_id=admin_id, person_id=person_id)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

# --- ACERCA DE MÍ ---
def get_about_me(session: Session, user_id: int) -> Optional[AboutMe]:
    statement = select(AboutMe).where(AboutMe.user_id == user_id)
    return session.exec(statement).first()

def create_or_update_about_me(session: Session, user_id: int, **kwargs) -> AboutMe:
    about_me = get_about_me(session, user_id)
    
    if about_me:
        # Actualizar campos
        for key, value in kwargs.items():
            if value is not None and hasattr(about_me, key):
                setattr(about_me, key, value)
        about_me.updated_at = datetime.utcnow()
    else:
        # Crear nuevo
        about_me = AboutMe(user_id=user_id, **kwargs)
        session.add(about_me)
    
    session.commit()
    session.refresh(about_me)
    return about_me

# --- EXPERIENCIA LABORAL ---
def create_work_experience(session: Session, user_id: int, **kwargs) -> WorkExperience:
    experience = WorkExperience(user_id=user_id, **kwargs)
    session.add(experience)
    session.commit()
    session.refresh(experience)
    return experience

def get_user_work_experiences(session: Session, user_id: int) -> List[WorkExperience]:
    statement = select(WorkExperience).where(WorkExperience.user_id == user_id)
    return session.exec(statement).all()

def update_work_experience(session: Session, experience_id: int, **kwargs) -> Optional[WorkExperience]:
    experience = session.get(WorkExperience, experience_id)
    if not experience:
        return None
    
    for key, value in kwargs.items():
        if value is not None and hasattr(experience, key):
            setattr(experience, key, value)
    
    experience.updated_at = datetime.utcnow()
    session.add(experience)
    session.commit()
    session.refresh(experience)
    return experience

def delete_work_experience(session: Session, experience_id: int) -> bool:
    experience = session.get(WorkExperience, experience_id)
    if experience:
        session.delete(experience)
        session.commit()
        return True
    return False

# --- EDUCACIÓN ---
def create_education(session: Session, user_id: int, **kwargs) -> Education:
    education = Education(user_id=user_id, **kwargs)
    session.add(education)
    session.commit()
    session.refresh(education)
    return education

def get_user_educations(session: Session, user_id: int) -> List[Education]:
    statement = select(Education).where(Education.user_id == user_id)
    return session.exec(statement).all()