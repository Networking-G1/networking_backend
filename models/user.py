# models/user.py
from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(index=True, nullable=False)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    role: str = Field(default="user")

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relaciones
    skills: List["UserSkill"] = Relationship(back_populates="user")