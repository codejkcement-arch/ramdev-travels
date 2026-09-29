from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Flight(Base):
    __tablename__ = "flights"
    id: Mapped[int] = mapped_column(primary_key=True)
    airline: Mapped[str] = mapped_column(String(120))
    flight_number: Mapped[str] = mapped_column(String(30), unique=True)
    source: Mapped[str] = mapped_column(String(100), index=True)
    destination: Mapped[str] = mapped_column(String(100), index=True)
    departure_time: Mapped[DateTime]
    arrival_time: Mapped[DateTime]
    fare: Mapped[float] = mapped_column(Float)
    available_seats: Mapped[int] = mapped_column(Integer, default=180)
