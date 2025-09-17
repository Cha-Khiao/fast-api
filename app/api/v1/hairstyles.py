from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.api.deps import get_db, require_admin
from app.models.hairstyle import Hairstyle
from app.models.review import Review
from app.schemas.hairstyle import HairstyleCreate, HairstyleUpdate, HairstyleOut

router = APIRouter(prefix="/hairstyles", tags=["hairstyles"])

@router.get("", response_model=List[HairstyleOut])
async def list_hairstyles(
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    offset = (page - 1) * limit
    stmt = select(
        Hairstyle.id, Hairstyle.name, Hairstyle.description, Hairstyle.image_url,
        func.avg(Review.rating).label("avg_rating")
    ).select_from(Hairstyle).join(Review, Review.hairstyle_id == Hairstyle.id, isouter=True)

    if search:
        stmt = stmt.where(Hairstyle.name.ilike(f"%{search}%"))

    stmt = stmt.group_by(Hairstyle.id).offset(offset).limit(limit)
    rows = (await db.execute(stmt)).all()

    return [
        HairstyleOut(
            id=r.id, name=r.name, description=r.description, image_url=r.image_url,
            avg_rating=float(r.avg_rating) if r.avg_rating is not None else None
        )
        for r in rows
    ]

@router.get("/{id}", response_model=HairstyleOut)
async def get_hairstyle(id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(
        Hairstyle, func.avg(Review.rating).label("avg_rating")
    ).join(Review, Review.hairstyle_id == Hairstyle.id, isouter=True).where(Hairstyle.id == id).group_by(Hairstyle.id)
    res = (await db.execute(stmt)).first()
    if not res:
        raise HTTPException(status_code=404, detail="Not found")
    hs, avg = res
    return HairstyleOut(
        id=hs.id, name=hs.name, description=hs.description, image_url=hs.image_url,
        avg_rating=float(avg) if avg is not None else None
    )

@router.post("", dependencies=[Depends(require_admin)], response_model=HairstyleOut)
async def create_hairstyle(payload: HairstyleCreate, db: AsyncSession = Depends(get_db)):
    hs = Hairstyle(name=payload.name, description=payload.description, image_url=payload.image_url)
    db.add(hs)
    await db.commit()
    await db.refresh(hs)
    return HairstyleOut(id=hs.id, name=hs.name, description=hs.description, image_url=hs.image_url, avg_rating=None)

@router.patch("/{id}", dependencies=[Depends(require_admin)], response_model=HairstyleOut)
async def update_hairstyle(id: str, payload: HairstyleUpdate, db: AsyncSession = Depends(get_db)):
    hs = await db.get(Hairstyle, id)
    if not hs:
        raise HTTPException(status_code=404, detail="Not found")
    if payload.name is not None:
        hs.name = payload.name
    if payload.description is not None:
        hs.description = payload.description
    if payload.image_url is not None:
        hs.image_url = payload.image_url
    await db.commit()
    await db.refresh(hs)
    return HairstyleOut(id=hs.id, name=hs.name, description=hs.description, image_url=hs.image_url, avg_rating=None)

@router.delete("/{id}", dependencies=[Depends(require_admin)])
async def delete_hairstyle(id: str, db: AsyncSession = Depends(get_db)):
    hs = await db.get(Hairstyle, id)
    if not hs:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(hs)
    await db.commit()
    return {"message": "Deleted"}
