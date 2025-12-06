# models/message.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    receiver_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    read: bool = Field(default=False, index=True)
    file_url: Optional[str] = Field(default=None)
    
    # Relaciones (opcional, para acceso fácil a los usuarios)
    # sender: Optional["User"] = Relationship()
    # receiver: Optional["User"] = Relationship()
