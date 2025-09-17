from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
