from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    firstname: Optional[str] = None   # ✅ เพิ่ม
    lastname: Optional[str] = None    # ✅ เพิ่ม

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class AccessToken(BaseModel):
    access_token: str

class RefreshRequest(BaseModel):
    refresh_token: str
