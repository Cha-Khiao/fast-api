from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteOut
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.get("", response_model=List[FavoriteOut])
async def list_favorites(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Favorite).where(Favorite.user_id == user.id))
    return [FavoriteOut.model_validate(f) for f in res.scalars().all()]

@router.post("", response_model=FavoriteOut)
async def add_favorite(payload: FavoriteCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(Favorite).where(Favorite.user_id == user.id, Favorite.hairstyle_id == payload.hairstyle_id))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already favorited")
    fav = Favorite(user_id=user.id, hairstyle_id=payload.hairstyle_id)
    db.add(fav)
    await db.commit()
    await db.refresh(fav)
    return FavoriteOut.model_validate(fav)

@router.delete("/{favorite_id}")
async def remove_favorite(favorite_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    fav = await db.get(Favorite, favorite_id)
    if not fav or fav.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(fav)
    await db.commit()
    return {"message": "Removed"}
