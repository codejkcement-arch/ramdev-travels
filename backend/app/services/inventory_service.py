from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bus import Seat
from app.models.cinema import CinemaSeat

async def reserve_bus_seats(db: AsyncSession, bus_id: int, seats: list[str]):
    wanted = list(dict.fromkeys(seats))
    if len(wanted) != len(seats):
        raise ValueError("Duplicate seats are not allowed")
    rows = (await db.scalars(select(Seat).where(Seat.bus_id == bus_id, Seat.seat_number.in_(wanted)).with_for_update())).all()
    if len(rows) != len(wanted) or any(s.is_booked for s in rows):
        raise ValueError("One or more seats are unavailable")
    for s in rows: s.is_booked = True
    return rows

async def reserve_cinema_seats(db: AsyncSession, show_id: int, seats: list[str]):
    wanted = list(dict.fromkeys(seats))
    if len(wanted) != len(seats):
        raise ValueError("Duplicate seats are not allowed")
    rows = (await db.scalars(select(CinemaSeat).where(CinemaSeat.show_id == show_id, CinemaSeat.seat_number.in_(wanted)).with_for_update())).all()
    if len(rows) != len(wanted) or any(s.is_booked for s in rows):
        raise ValueError("One or more seats are unavailable")
    for s in rows: s.is_booked = True
    return rows

async def release_bus_seats(db: AsyncSession, bus_id: int, seats: list[str]):
    await db.execute(update(Seat).where(Seat.bus_id == bus_id, Seat.seat_number.in_(seats)).values(is_booked=False))

async def release_cinema_seats(db: AsyncSession, show_id: int, seats: list[str]):
    await db.execute(update(CinemaSeat).where(CinemaSeat.show_id == show_id, CinemaSeat.seat_number.in_(seats)).values(is_booked=False))
