from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.models.user import User

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/{hairstyle_id}", response_model=List[ReviewOut])
async def list_reviews(hairstyle_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Review).where(Review.hairstyle_id == hairstyle_id))
    return [ReviewOut.model_validate(r) for r in res.scalars().all()]

@router.post("", response_model=ReviewOut)
async def create_review(payload: ReviewCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rev = Review(user_id=user.id, hairstyle_id=payload.hairstyle_id, rating=payload.rating, comment=payload.comment)
    db.add(rev)
    await db.commit()
    await db.refresh(rev)
    return ReviewOut.model_validate(rev)

@router.patch("/{review_id}", response_model=ReviewOut)
async def update_review(review_id: str, payload: ReviewUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rev = await db.get(Review, review_id)
    if not rev or str(rev.user_id) != str(user.id):
        raise HTTPException(status_code=404, detail="Not found")
    if payload.rating is not None:
        rev.rating = payload.rating
    if payload.comment is not None:
        rev.comment = payload.comment
    await db.commit()
    await db.refresh(rev)
    return ReviewOut.model_validate(rev)

@router.delete("/{review_id}")
async def delete_review(review_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rev = await db.get(Review, review_id)
    if not rev or str(rev.user_id) != str(user.id):
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(rev)
    await db.commit()
    return {"message": "Deleted"}
