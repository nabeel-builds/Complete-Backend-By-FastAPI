from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=72)

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)