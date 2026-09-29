from sqlalchemy import String, Integer, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Cinema(Base):
    __tablename__ = "cinemas"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    city: Mapped[str] = mapped_column(String(100), index=True)
    address: Mapped[str] = mapped_column(String(255))

class CinemaShow(Base):
    __tablename__ = "cinema_shows"
    id: Mapped[int] = mapped_column(primary_key=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"))
    movie_name: Mapped[str] = mapped_column(String(150))
    show_time: Mapped[DateTime]
    price: Mapped[float] = mapped_column(Float)
    total_seats: Mapped[int] = mapped_column(Integer, default=100)
    cinema = relationship("Cinema")

class CinemaSeat(Base):
    __tablename__ = "cinema_seats"
    id: Mapped[int] = mapped_column(primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey("cinema_shows.id", ondelete="CASCADE"))
    seat_number: Mapped[str] = mapped_column(String(10))
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False)
