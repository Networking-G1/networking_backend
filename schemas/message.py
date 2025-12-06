# schemas/message.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    receiver_id: int
    content: str
    file_url: Optional[str] = None

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime
    read: bool
    file_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserBasic(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: str
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    other_user: UserBasic
    last_message: MessageResponse
