from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.extra import SkillType, ActivityType


# -----------------------------
#  SKILLS
# -----------------------------

class SkillBase(BaseModel):
    name: str
    type: SkillType
    level: Optional[int] = 1  # 1–5


class SkillCreate(SkillBase):
    pass


class SkillRead(SkillBase):
    id: int

    class Config:
        orm_mode = True


# -----------------------------
#  HOBBIES
# -----------------------------

class HobbyBase(BaseModel):
    name: str


class HobbyCreate(HobbyBase):
    pass


class HobbyRead(HobbyBase):
    id: int

    class Config:
        orm_mode = True


# -----------------------------
#  ADMIN MONITORING
# -----------------------------

class AdminMonitorBase(BaseModel):
    admin_id: int
    user_id: int


class AdminMonitorCreate(AdminMonitorBase):
    pass


class AdminMonitorRead(AdminMonitorBase):
    id: int

    class Config:
        orm_mode = True


# -----------------------------
#  JOB APPLICATIONS
# -----------------------------

class JobApplicationCreate(BaseModel):
    user_id: int
    job_id: int


class JobApplicationRead(BaseModel):
    id: int
    user_id: int
    job_id: int
    applied_at: datetime
    status: str
    hired: bool

    class Config:
        orm_mode = True


# -----------------------------
#  MESSAGES
# -----------------------------

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    content: str


class MessageRead(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


# -----------------------------
#  ACTIVITY LOG
# -----------------------------

class ActivityLogCreate(BaseModel):
    user_id: int
    type: ActivityType
    details: Optional[str] = None


class ActivityLogRead(BaseModel):
    id: int
    user_id: int
    type: ActivityType
    details: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


# -----------------------------
#  CONNECTION REQUESTS
# -----------------------------

class ConnectionRequestCreate(BaseModel):
    recipient_id: int
