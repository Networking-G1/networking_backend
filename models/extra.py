# models/extra.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

# -------- ENUMS ---------

class SkillType(str, Enum):
    hard = "hard"
    soft = "soft"

# -------- MODELO SKILL ---------

class Skill(SQLModel, table=True):
    __tablename__ = "skill"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    type: SkillType = Field(default=SkillType.hard)

    # relación inversa hacia UserSkill
    users: List["UserSkill"] = Relationship(back_populates="skill")

# -------- TABLA INTERMEDIA USER-SKILL ---------

class UserSkill(SQLModel, table=True):
    __tablename__ = "userskill"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill.id", primary_key=True)
    level: Optional[int] = Field(default=1)   # nivel 1–5 recomendado
    endorsements: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    user: "User" = Relationship(back_populates="skills")
    skill: Skill = Relationship(back_populates="users")

class Hobby(SQLModel, table=True):
    __tablename__ = "hobby"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)

class UserHobby(SQLModel, table=True):
    __tablename__ = "userhobby"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    hobby_id: int = Field(foreign_key="hobby.id")

class Preference(SQLModel, table=True):
    __tablename__ = "preference"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    key: str = Field(nullable=False)   # e.g. "remote", "looking_for", "salary_min"
    value: str = Field(nullable=False) # store as string or json

class ActivityType(str, Enum):
    login = "login"
    apply_job = "apply_job"
    view_job = "view_job"
    message_sent = "message_sent"
    profile_update = "profile_update"

class ActivityLog(SQLModel, table=True):
    __tablename__ = "activitylog"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    type: ActivityType
    details: Optional[str] = None  # <--- renombrado
    created_at: datetime = Field(default_factory=datetime.utcnow)


class JobApplicationStatus(str, Enum):
    applied = "applied"
    interviewed = "interviewed"
    hired = "hired"
    rejected = "rejected"

class JobApplication(SQLModel, table=True):
    __tablename__ = "jobapplication"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    job_id: int = Field(index=True)  # job id from external jobs service
    status: JobApplicationStatus = Field(default=JobApplicationStatus.applied)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AdminMonitor(SQLModel, table=True):
    __tablename__ = "adminmonitor"
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="users.id", index=True)
    person_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    __tablename__ = "message"
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    sender_id: int = Field(foreign_key="users.id", index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read: bool = Field(default=False)
