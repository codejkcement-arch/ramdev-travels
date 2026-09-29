import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.booking import Booking
from app.models.bus import Bus
from app.models.flight import Flight
from app.models.cinema import CinemaShow
from app.services.inventory_service import (
    reserve_bus_seats, reserve_cinema_seats, release_bus_seats, release_cinema_seats
)
from app.config import settings

async def expire_booking_holds(db: AsyncSession) -> int:
    """Release expired inventory inside the current DB transaction.

    This makes the free deployment independent of Redis/Celery. Expired holds
    are cleaned up whenever booking/search traffic reaches the API.
    """
    now = datetime.now(timezone.utc)
    rows = (await db.scalars(
        select(Booking)
        .where(Booking.status == "PENDING", Booking.hold_expires_at.is_not(None), Booking.hold_expires_at <= now)
        .with_for_update()
    )).all()
    if not rows:
        return 0
    for booking in rows:
        seats = booking.seats.split(",") if booking.seats else []
        if booking.booking_type == "bus":
            await release_bus_seats(db, booking.item_id, seats)
        elif booking.booking_type == "cinema":
            await release_cinema_seats(db, booking.item_id, seats)
        elif booking.booking_type == "flight":
            flight = await db.get(Flight, booking.item_id, with_for_update=True)
            if flight:
                flight.available_seats += len(seats)
        booking.status = "EXPIRED"
        booking.payment_status = "EXPIRED"
        booking.hold_expires_at = None
    return len(rows)


def pnr():
    return "RDT" + secrets.token_hex(4).upper()

async def create_booking(db: AsyncSession, user_id: int, booking_type: str, item_id: int, seats: list[str]):
    seats = list(dict.fromkeys(s.strip().upper() for s in seats if s.strip()))
    if not seats or len(seats) > 10:
        raise ValueError("Select between 1 and 10 seats")
    await expire_booking_holds(db)
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.BOOKING_HOLD_MINUTES)
    if booking_type == "bus":
        item = await db.scalar(select(Bus).where(Bus.id == item_id).with_for_update())
        if not item: raise ValueError("Bus not found")
        await reserve_bus_seats(db, item_id, seats)
        amount = item.fare * len(seats)
    elif booking_type == "flight":
        item = await db.scalar(select(Flight).where(Flight.id == item_id).with_for_update())
        if not item or item.available_seats < len(seats): raise ValueError("Flight unavailable")
        item.available_seats -= len(seats)
        amount = item.fare * len(seats)
    elif booking_type == "cinema":
        item = await db.scalar(select(CinemaShow).where(CinemaShow.id == item_id).with_for_update())
        if not item: raise ValueError("Show not found")
        await reserve_cinema_seats(db, item_id, seats)
        amount = item.price * len(seats)
    else:
        raise ValueError("Unsupported booking type")
    booking = Booking(pnr=pnr(), user_id=user_id, booking_type=booking_type, item_id=item_id,
                      seats=",".join(seats), amount=amount, hold_expires_at=expires)
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking
