from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.routes.auth import current_user
from app.models.booking import Booking
from app.models.payment import Payment
from app.schemas.payment import CreateOrderRequest, VerifyPaymentRequest
from app.services.payment_service import create_order
from app.config import settings
from app.services.booking_service import expire_booking_holds
from app.utils.razorpay_utils import verify_razorpay_signature
from datetime import datetime, timezone

router = APIRouter()

@router.post("/create-order")
async def make_order(data: CreateOrderRequest, user=Depends(current_user), db: AsyncSession = Depends(get_db)):
    await expire_booking_holds(db)
    await db.commit()
    booking = await db.get(Booking, data.booking_id)
    if not booking or booking.user_id != user.id: raise HTTPException(404, "Booking not found")
    if booking.payment_status == "PAID": raise HTTPException(400, "Booking already paid")
    if booking.hold_expires_at and booking.hold_expires_at <= datetime.now(timezone.utc):
        raise HTTPException(409, "Booking hold expired; please create a new booking")
    try: order = create_order(booking.amount, booking.pnr)
    except RuntimeError as exc: raise HTTPException(503, str(exc))
    payment = await db.scalar(select(Payment).where(Payment.booking_id == booking.id))
    if not payment:
        payment = Payment(booking_id=booking.id, amount=booking.amount, order_id=order["id"])
        db.add(payment)
    else:
        payment.order_id, payment.amount, payment.status = order["id"], booking.amount, "CREATED"
    await db.commit()
    return {"key_id": settings.RAZORPAY_KEY_ID, "order_id": order["id"], "amount": order["amount"], "currency": order["currency"]}

@router.post("/verify")
async def verify(data: VerifyPaymentRequest, user=Depends(current_user), db: AsyncSession = Depends(get_db)):
    booking = await db.get(Booking, data.booking_id)
    if not booking or booking.user_id != user.id: raise HTTPException(404, "Booking not found")
    payment = await db.scalar(select(Payment).where(Payment.booking_id == booking.id))
    if not payment or payment.order_id != data.razorpay_order_id:
        raise HTTPException(400, "Payment order mismatch")
    if payment.amount != booking.amount:
        raise HTTPException(400, "Payment amount mismatch")
    if booking.payment_status == "PAID":
        return {"message": "Payment already verified", "pnr": booking.pnr}
    if not verify_razorpay_signature(data.razorpay_order_id, data.razorpay_payment_id, data.razorpay_signature):
        raise HTTPException(400, "Invalid payment signature")
    payment.payment_id = data.razorpay_payment_id
    payment.signature = data.razorpay_signature
    payment.status = "PAID"
    booking.payment_status = "PAID"
    booking.status = "CONFIRMED"
    booking.hold_expires_at = None
    await db.commit()
    return {"message": "Payment verified", "pnr": booking.pnr}
