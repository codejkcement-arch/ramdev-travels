from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.cinema import Cinema, CinemaShow, CinemaSeat
from app.services.booking_service import expire_booking_holds

router = APIRouter()

@router.get("/search")
async def search(city: str, movie: str | None = None, db: AsyncSession = Depends(get_db)):
    await expire_booking_holds(db)
    await db.commit()
    stmt = select(CinemaShow, Cinema).join(Cinema, Cinema.id == CinemaShow.cinema_id).where(Cinema.city.ilike(f"%{city}%"))
    if movie:
        stmt = stmt.where(CinemaShow.movie_name.ilike(f"%{movie}%"))
    rows = (await db.execute(stmt)).all()
    return [{"id": show.id, "cinema_id": cinema.id, "cinema": cinema.name, "city": cinema.city,
             "address": cinema.address, "movie_name": show.movie_name, "show_time": show.show_time,
             "price": show.price, "total_seats": show.total_seats} for show, cinema in rows]

@router.get("/{show_id}/seats")
async def seats(show_id: int, db: AsyncSession = Depends(get_db)):
    await expire_booking_holds(db)
    await db.commit()
    rows = await db.scalars(select(CinemaSeat).where(CinemaSeat.show_id == show_id).order_by(CinemaSeat.seat_number))
    return [{"id": s.id, "seat_number": s.seat_number, "is_booked": s.is_booked} for s in rows.all()]
