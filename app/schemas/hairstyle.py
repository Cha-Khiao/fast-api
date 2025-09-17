from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class HairstyleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class HairstyleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class HairstyleOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    avg_rating: Optional[float] = None

    class Config:
        from_attributes = True
