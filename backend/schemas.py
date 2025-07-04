from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    phone_number: str = Field(..., example="13800138000")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="strongpassword123")
    verification_code: str = Field(..., example="123456")

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- SMS Schemas ---
class SendSMSRequest(BaseModel):
    phone_number: str
    purpose: str = Field(..., example="REGISTER or RESET_PASSWORD")

class SMSLogOut(BaseModel):
    id: int
    phone_number: str
    content: str
    status: str
    sent_at: datetime

    class Config:
        orm_mode = True

# --- Password Reset ---
class ResetPasswordRequest(BaseModel):
    phone_number: str
    verification_code: str
    new_password: str = Field(..., min_length=6)