from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base

class Refund(Base):
    __tablename__ = "refunds"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    amount: Mapped[float] = mapped_column(Float)
    reason: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="REQUESTED")
    provider_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
