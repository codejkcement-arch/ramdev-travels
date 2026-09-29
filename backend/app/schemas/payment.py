from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    booking_id: int

class VerifyPaymentRequest(BaseModel):
    booking_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

class PaymentOut(BaseModel):
    order_id: str | None
    payment_id: str | None
    amount: float
    currency: str
    status: str
    model_config = {"from_attributes": True}
