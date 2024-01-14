from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: int
    email: EmailStr
    created_at: datetime


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserLogin(UserBase):
    email: EmailStr
    password: str
