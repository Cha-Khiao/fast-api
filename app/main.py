from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.hairstyles import router as hairstyles_router
from app.api.v1.favorites import router as favorites_router
from app.api.v1.reviews import router as reviews_router
from app.core.config import settings
from app.db.session import engine
from app.models.base import Base

app = FastAPI(title="CutMatch API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(hairstyles_router, prefix="/api/v1")
app.include_router(favorites_router, prefix="/api/v1")
app.include_router(reviews_router, prefix="/api/v1")
