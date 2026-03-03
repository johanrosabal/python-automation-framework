# api_mock/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    age: Optional[int] = None


class User(UserCreate):
    id: int
