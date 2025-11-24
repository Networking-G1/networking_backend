# models/user.py
from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

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