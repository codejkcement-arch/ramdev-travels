from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.education.db.session import get_db

router = APIRouter()

@router.get("/admin")
async def admin_dashboard(db: AsyncSession = Depends(get_db)):
    queries = {
        "students": "SELECT count(*) FROM education.user_roles ur JOIN education.roles r ON r.id=ur.role_id WHERE r.code='student'",
        "teachers": "SELECT count(*) FROM education.user_roles ur JOIN education.roles r ON r.id=ur.role_id WHERE r.code='teacher'",
        "courses": "SELECT count(*) FROM education.courses WHERE deleted_at IS NULL",
        "tests": "SELECT count(*) FROM education.tests",
    }
    out = {}
    for key, sql in queries.items():
        out[key] = (await db.execute(text(sql))).scalar_one()
    return out
