from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.routes.auth import current_user
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking_service import create_booking

router = APIRouter()

def serialize(b):
    return {**b.__dict__, "seats": b.seats.split(",")}

@router.post("", response_model=BookingOut)
async def create(data: BookingCreate, user=Depends(current_user), db: AsyncSession = Depends(get_db)):
    try:
        b = await create_booking(db, user.id, data.booking_type, data.item_id, data.seats)
        return serialize(b)
    except ValueError as e:
        await db.rollback()
        raise HTTPException(400, str(e))

@router.get("", response_model=list[BookingOut])
async def history(user=Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(Booking).where(Booking.user_id == user.id).order_by(Booking.id.desc()))
    return [serialize(b) for b in result.all()]

@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(booking_id: int, user=Depends(current_user), db: AsyncSession = Depends(get_db)):
    b = await db.get(Booking, booking_id)
    if not b or b.user_id != user.id:
        raise HTTPException(404, "Booking not found")
    return serialize(b)
