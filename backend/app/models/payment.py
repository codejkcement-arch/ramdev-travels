from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    provider: Mapped[str] = mapped_column(String(30), default="razorpay")
    order_id: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    payment_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    signature: Mapped[str | None] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(5), default="INR")
    status: Mapped[str] = mapped_column(String(30), default="CREATED")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    booking = relationship("Booking", back_populates="payment")
