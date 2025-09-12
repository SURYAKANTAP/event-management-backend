# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .enums import UserRole

# For Events
class EventBase(BaseModel):
    title: str
    description: str
    date: str
    time: str
    image_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# For Users
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.normal

class User(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

# For Authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserRoleUpdate(BaseModel):
    role: UserRole