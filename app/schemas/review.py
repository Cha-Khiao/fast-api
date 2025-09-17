from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ReviewCreate(BaseModel):
    hairstyle_id: UUID
    rating: int
    comment: Optional[str] = None

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewOut(BaseModel):
    id: UUID
    user_id: UUID
    hairstyle_id: UUID
    rating: int
    comment: Optional[str] = None

    class Config:
        from_attributes = True
