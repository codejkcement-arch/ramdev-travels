from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.routes.auth import admin_user
from app.models.user import User
from app.models.booking import Booking
from app.models.refund import Refund
from app.models.payment import Payment
from app.services.payment_service import refund_payment

router = APIRouter()

@router.get("/stats")
async def stats(admin=Depends(admin_user), db: AsyncSession = Depends(get_db)):
    users = await db.scalar(select(func.count(User.id)))
    bookings = await db.scalar(select(func.count(Booking.id)))
    revenue = await db.scalar(select(func.coalesce(func.sum(Booking.amount), 0)).where(Booking.payment_status == "PAID"))
    return {"users": users, "bookings": bookings, "revenue": float(revenue or 0)}

@router.get("/bookings")
async def bookings(admin=Depends(admin_user), db: AsyncSession = Depends(get_db)):
    rows = await db.scalars(select(Booking).options(selectinload(Booking.payment)).order_by(Booking.id.desc()).limit(200))
    return [{"id": b.id, "pnr": b.pnr, "type": b.booking_type, "amount": b.amount,
             "status": b.status, "payment_status": b.payment_status} for b in rows.all()]

@router.post("/refund/{booking_id}")
async def refund(booking_id: int, admin=Depends(admin_user), db: AsyncSession = Depends(get_db)):
    b = await db.get(Booking, booking_id)
    if not b or b.payment_status != "PAID":
        raise HTTPException(400, "Paid booking not found")
    refund = Refund(booking_id=b.id, amount=b.amount, reason="Admin initiated")
    payment = await db.scalar(select(__import__("app.models.payment", fromlist=["Payment"]).Payment).where(__import__("app.models.payment", fromlist=["Payment"]).Payment.booking_id == b.id))
    if not payment or not payment.payment_id:
        raise HTTPException(400, "Payment reference missing")
    try:
        result = refund_payment(payment.payment_id, b.amount)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))
    refund.provider_ref = result.get("id")
    refund.status = "PROCESSED"
    b.status = "REFUNDED"
    b.payment_status = "REFUNDED"
    db.add(refund)
    await db.commit()
    return {"message": "Refund processed", "refund_id": refund.id}
