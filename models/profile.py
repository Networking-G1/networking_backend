# backend/models/profile.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING  
from datetime import date, datetime
from enum import Enum

# Evita importación circular
if TYPE_CHECKING:
    from models.user import User

class AboutMe(SQLModel, table=True):
    __tablename__ = "about_me"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    bio: Optional[str] = Field(default=None, max_length=2000)
    summary: Optional[str] = Field(default=None, max_length=500)
    location: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    linkedin: Optional[str] = Field(default=None)
    github: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional["User"] = Relationship(back_populates="about_me")

class WorkExperience(SQLModel, table=True):
    __tablename__ = "work_experience"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    company: str = Field(max_length=200)
    location: Optional[str] = Field(default=None)
    start_date: date
    end_date: Optional[date] = Field(default=None)
    currently_working: bool = Field(default=False)
    description: Optional[str] = Field(default=None, max_length=2000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional["User"] = Relationship(back_populates="work_experiences")

class Education(SQLModel, table=True):
    __tablename__ = "education"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    institution: str = Field(max_length=200)
    degree: str = Field(max_length=200)
    field_of_study: Optional[str] = Field(default=None, max_length=200)
    start_date: date
    end_date: Optional[date] = Field(default=None)
    currently_studying: bool = Field(default=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional["User"] = Relationship(back_populates="educations")

