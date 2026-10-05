from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.education.db.session import get_db

router = APIRouter()

@router.get("/me")
async def me(db: AsyncSession = Depends(get_db)):
    # Replace with JWT dependency after wiring login in production.
    return {"message": "Auth module ready", "next": "POST /auth/login"}
