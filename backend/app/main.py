from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.models.user import User
from app.utils.security import hash_password
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.routes import auth, buses, flights, cinema, bookings, payments, admin, webhooks

async def ensure_admin_user():
    if not settings.ADMIN_EMAIL or not settings.ADMIN_PASSWORD:
        return
    async with AsyncSessionLocal() as db:
        user = await db.scalar(select(User).where(User.email == settings.ADMIN_EMAIL))
        if user:
            if not user.is_admin:
                user.is_admin = True
                await db.commit()
        else:
            db.add(User(name="Admin", email=settings.ADMIN_EMAIL, password_hash=hash_password(settings.ADMIN_PASSWORD), is_admin=True))
            await db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.AUTO_CREATE_TABLES:
        await init_db()
    await ensure_admin_user()
    yield

app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_origin_regex=settings.CORS_ORIGIN_REGEX, allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(buses.router, prefix="/api/buses", tags=["buses"])
app.include_router(flights.router, prefix="/api/flights", tags=["flights"])
app.include_router(cinema.router, prefix="/api/cinema", tags=["cinema"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}
