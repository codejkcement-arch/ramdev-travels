import razorpay
from app.config import settings

def client():
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return None
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(amount: float, receipt: str):
    c = client()
    if not c: raise RuntimeError("Razorpay is not configured")
    return c.order.create({"amount": int(round(amount * 100)), "currency": "INR", "receipt": receipt})

def refund_payment(payment_id: str, amount: float):
    c = client()
    if not c: raise RuntimeError("Razorpay is not configured")
    return c.payment.refund(payment_id, {"amount": int(round(amount * 100))})
