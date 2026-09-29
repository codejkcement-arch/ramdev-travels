import hmac, hashlib
from app.config import settings

def verify_razorpay_signature(order_id: str, payment_id: str, signature: str) -> bool:
    message = f"{order_id}|{payment_id}".encode()
    expected = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

def verify_webhook_signature(body: bytes, signature: str) -> bool:
    expected = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
