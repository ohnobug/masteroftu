from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime


class BaseResponse(BaseModel):
    code: int = Field(..., example=200)
    message: str = Field(..., example="Success")

# --- User Schemas ---
class UserBase(BaseModel):
    phone_number: str = Field(..., example="13800138000")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="strongpassword123")
    verification_code: str = Field(..., example="123456")

class UserLogin(BaseModel):
    phone_number: str
    password: str


class UserRegisterRequestOut(BaseResponse):
    pass
    
class UserRegisterRequestIn(BaseModel):
    phone_number: str = Field(...)
    password: str = Field(...)
    verification_code: str = Field(...)



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
        from_attributes = True

# --- Password Reset ---
class ResetPasswordRequest(BaseModel):
    phone_number: str
    verification_code: str
    new_password: str = Field(..., min_length=6)
    

class UserInfoRequestOut(BaseModel):
    username: str = Field(..., example="")

class UserInfoRequestIn(BaseModel):
    username: str = Field(..., example="")

class UserLoginRequestIn(BaseModel):
    phone_number: str = Field(..., example="")
    password: str = Field(..., example="")

class UserLoginToken(BaseModel):
    token: str = Field(...)

class UserLoginRequestOut(BaseResponse):
    data: UserLoginToken = Field(...)



class ChatSessionIn(BaseModel):
    pass

class ChatSession(BaseModel):
    id: int
    title: str

class ChatSessionOut(BaseResponse):
    data: Dict[int, ChatSession] = Field(...)

class ChatHistoryIn(BaseModel):
    chat_session_id: int = Field(..., example=1)

class ChatHistory(BaseModel):
    id: int
    sender: str
    text: str
    created_at: int

class ChatHistoryOut(BaseResponse):
    data: Dict[int, ChatHistory] = Field(...)


class ChatNewsessionIn(BaseModel):
    title: str = Field(...)

class ChatNewsession(BaseModel):
    chat_session_id: int

class ChatNewsessionOut(BaseResponse):
    data: ChatNewsession = Field(...)


class ChatNewmessageIn(BaseModel):
    chat_session_id: int = Field(...)
    text: str

class ChatNewmessage(BaseModel):
    chat_message_id: int
    ai_message_id: int

class ChatNewmessageOut(BaseResponse):
    data: ChatNewmessage = Field(...)


class ChatDelsessionIn(BaseModel):
    chat_session_id: int = Field(...)

class ChatDelsessionOut(BaseResponse):
    pass