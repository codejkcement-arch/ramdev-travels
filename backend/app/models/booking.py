from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    pnr: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    booking_type: Mapped[str] = mapped_column(String(20))
    item_id: Mapped[int] = mapped_column(Integer)
    seats: Mapped[str] = mapped_column(Text)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30), default="PENDING")
    payment_status: Mapped[str] = mapped_column(String(30), default="PENDING")
    hold_expires_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan")
