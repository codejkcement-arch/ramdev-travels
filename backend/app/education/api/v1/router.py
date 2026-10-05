from fastapi import APIRouter
from app.education.api.v1 import auth, courses, tests, dashboard

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(tests.router, prefix="/tests", tags=["Tests"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
