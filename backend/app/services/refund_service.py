from app.services.payment_service import refund_payment
async def process_refund(payment_id: str, amount: float):
    return refund_payment(payment_id, amount)
