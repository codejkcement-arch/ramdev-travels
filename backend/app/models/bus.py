from sqlalchemy import String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Bus(Base):
    __tablename__ = "buses"
    id: Mapped[int] = mapped_column(primary_key=True)
    operator: Mapped[str] = mapped_column(String(120))
    bus_number: Mapped[str] = mapped_column(String(50), unique=True)
    source: Mapped[str] = mapped_column(String(100), index=True)
    destination: Mapped[str] = mapped_column(String(100), index=True)
    departure_time: Mapped[str] = mapped_column(String(10))
    arrival_time: Mapped[str] = mapped_column(String(10))
    fare: Mapped[float] = mapped_column(Float)
    total_seats: Mapped[int] = mapped_column(Integer, default=40)
    seats = relationship("Seat", back_populates="bus", cascade="all, delete-orphan")

class Seat(Base):
    __tablename__ = "bus_seats"
    id: Mapped[int] = mapped_column(primary_key=True)
    bus_id: Mapped[int] = mapped_column(ForeignKey("buses.id", ondelete="CASCADE"))
    seat_number: Mapped[str] = mapped_column(String(10))
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False)
    bus = relationship("Bus", back_populates="seats")
