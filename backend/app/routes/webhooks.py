import hashlib, hmac, json
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select
from app.config import settings
from app.database import AsyncSessionLocal
from app.models.booking import Booking
from app.models.payment import Payment
from app.utils.razorpay_utils import verify_webhook_signature

router = APIRouter()

@router.post("/razorpay")
async def razorpay_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")
    if not settings.RAZORPAY_WEBHOOK_SECRET: raise HTTPException(503, "Razorpay webhook secret is not configured")
    if not verify_webhook_signature(body, signature): raise HTTPException(400, "Invalid webhook signature")
    event = json.loads(body.decode("utf-8"))
    async with AsyncSessionLocal() as db:
        order_id = event.get("payload", {}).get("payment", {}).get("entity", {}).get("order_id")
        payment_id = event.get("payload", {}).get("payment", {}).get("entity", {}).get("id")
        if order_id:
            payment = await db.scalar(select(Payment).where(Payment.order_id == order_id))
            if payment and event.get("event") in {"payment.captured", "order.paid"}:
                booking = await db.get(Booking, payment.booking_id)
                if booking and booking.payment_status != "PAID":
                    payment.payment_id = payment_id or payment.payment_id
                    payment.status = "PAID"
                    booking.payment_status = "PAID"
                    booking.status = "CONFIRMED"
                    booking.hold_expires_at = None
                    await db.commit()
    return {"status": "received", "event": event.get("event")}
