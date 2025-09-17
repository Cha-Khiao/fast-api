from pydantic import BaseModel
from uuid import UUID

class FavoriteCreate(BaseModel):
    hairstyle_id: UUID

class FavoriteOut(BaseModel):
    id: UUID
    hairstyle_id: UUID

    class Config:
        from_attributes = True
