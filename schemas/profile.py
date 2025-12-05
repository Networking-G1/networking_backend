# backend/schemas/profile.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class AboutMeCreate(BaseModel):
    bio: Optional[str] = Field(None, max_length=2000)
    summary: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class WorkExperienceCreate(BaseModel):
    title: str = Field(..., max_length=200)
    company: str = Field(..., max_length=200)
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    currently_working: bool = False
    description: Optional[str] = Field(None, max_length=2000)

class WorkExperienceUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    company: Optional[str] = Field(None, max_length=200)
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    currently_working: Optional[bool] = None
    description: Optional[str] = Field(None, max_length=2000)

class EducationCreate(BaseModel):
    institution: str = Field(..., max_length=200)
    degree: str = Field(..., max_length=200)
    field_of_study: Optional[str] = Field(None, max_length=200)
    start_date: date
    end_date: Optional[date] = None
    currently_studying: bool = False
    description: Optional[str] = Field(None, max_length=1000)

class WorkExperienceOut(BaseModel):
    id: int
    user_id: int
    title: str
    company: str
    location: Optional[str]
    start_date: date
    end_date: Optional[date]
    currently_working: bool
    description: Optional[str]

    class Config:
        orm_mode = True

class EducationOut(BaseModel):
    id: int
    user_id: int
    institution: str
    degree: str
    field_of_study: Optional[str]
    start_date: date
    end_date: Optional[date]
    currently_studying: bool
    description: Optional[str]

    class Config:
        orm_mode = True

class AboutMeOut(BaseModel):
    id: Optional[int]
    user_id: int
    bio: Optional[str]
    summary: Optional[str]
    location: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]

    class Config:
        orm_mode = True