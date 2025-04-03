from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: Optional[str] = None
    created_at: datetime
    confirmed: bool

    class Config:
        orm_mode = True


class RequestEmail(BaseModel):
    email: EmailStr


class EmailSchema(BaseModel):
    email: EmailStr
