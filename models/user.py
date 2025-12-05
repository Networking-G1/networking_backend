# models/user.py
from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
from models.profile import AboutMe, WorkExperience, Education
from models.extra import UserSkill

class UserRole(str, Enum):
    person = "person"
    company = "company"
    admin = "admin"

class UserBase(SQLModel):
    email: str = Field(index=True, nullable=False)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    role: UserRole = Field(default=UserRole.person)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relaciones
    skills: List["UserSkill"] = Relationship(back_populates="user")

    # NUEVAS relaciones para perfil profesional
    about_me: Optional["AboutMe"] = Relationship(back_populates="user")
    work_experiences: List["WorkExperience"] = Relationship(back_populates="user")
    educations: List["Education"] = Relationship(back_populates="user")