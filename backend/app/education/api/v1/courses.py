from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.education.db.session import get_db

router = APIRouter()

@router.get("")
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text(
        "SELECT id, code, title, slug, description, thumbnail_url, price, is_free "
        "FROM education.courses WHERE deleted_at IS NULL AND status='published' "
        "ORDER BY created_at DESC"
    ))
    return [dict(r._mapping) for r in result.all()]

@router.get("/{course_id}")
async def get_course(course_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text(
        "SELECT id, code, title, slug, description, thumbnail_url, price, is_free "
        "FROM education.courses WHERE id=:id AND deleted_at IS NULL"
    ), {"id": course_id})
    row = result.first()
    return dict(row._mapping) if row else {"detail": "Course not found"}
