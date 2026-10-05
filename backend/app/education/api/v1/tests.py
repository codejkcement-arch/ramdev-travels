from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.education.db.session import get_db

router = APIRouter()

@router.get("")
async def list_tests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text(
        "SELECT id, title, duration_minutes, total_marks, total_questions "
        "FROM education.tests WHERE status='published' ORDER BY created_at DESC"
    ))
    return [dict(r._mapping) for r in result.all()]

@router.get("/{test_id}/questions")
async def test_questions(test_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text(
        "SELECT q.id, q.question_no, q.body, q.question_type, q.marks, "
        "json_agg(json_build_object('id',o.id,'key',o.option_key,'text',o.option_text) "
        "ORDER BY o.option_key) AS options "
        "FROM education.questions q "
        "LEFT JOIN education.question_options o ON o.question_id=q.id "
        "WHERE q.test_id=:id GROUP BY q.id ORDER BY q.question_no"
    ), {"id": test_id})
    return [dict(r._mapping) for r in result.all()]
