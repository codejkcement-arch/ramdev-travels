from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models.user import User
from app.schemas.user import RegisterRequest, LoginRequest, UserOut
from app.schemas.common import Token
from app.utils.security import hash_password, verify_password, create_access_token, decode_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if not payload or not payload.get("sub"):
        raise HTTPException(401, "Invalid or expired token")
    user = await db.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(401, "User not found")
    return user

async def admin_user(user=Depends(current_user)):
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")
    return user

@router.post("/register", response_model=UserOut)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    exists = await db.scalar(select(User).where(User.email == data.email))
    if exists:
        raise HTTPException(409, "Email already registered")
    user = User(name=data.name, email=data.email, phone=data.phone, password_hash=hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == data.email))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def me(user=Depends(current_user)):
    return user
