# models/groups.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Group(SQLModel, table=True):
    __tablename__ = "groups"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    members: List["UserGroup"] = Relationship(back_populates="group")

class Job(SQLModel, table=True):
    __tablename__ = "jobs"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[int] = Field(foreign_key="users.id")

    # Relación con owner
    owner: Optional["User"] = Relationship()

class UserGroup(SQLModel, table=True):
    __tablename__ = "user_groups"
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    group_id: int = Field(foreign_key="groups.id", primary_key=True)

    # Relaciones
    user: "User" = Relationship()
    group: Group = Relationship(back_populates="members")