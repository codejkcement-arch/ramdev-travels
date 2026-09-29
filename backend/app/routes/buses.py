from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database import get_db
from app.models.bus import Bus, Seat
from app.services.booking_service import expire_booking_holds

router = APIRouter()

@router.get("/search")
async def search(source: str, destination: str, db: AsyncSession = Depends(get_db)):
    await expire_booking_holds(db)
    await db.commit()
    result = await db.scalars(select(Bus).where(
        and_(Bus.source.ilike(f"%{source}%"), Bus.destination.ilike(f"%{destination}%"))
    ))
    buses = result.all()
    return [{"id": b.id, "operator": b.operator, "bus_number": b.bus_number,
             "source": b.source, "destination": b.destination,
             "departure_time": b.departure_time, "arrival_time": b.arrival_time,
             "fare": b.fare, "total_seats": b.total_seats} for b in buses]

@router.get("/{bus_id}/seats")
async def seats(bus_id: int, db: AsyncSession = Depends(get_db)):
    await expire_booking_holds(db)
    await db.commit()
    result = await db.scalars(select(Seat).where(Seat.bus_id == bus_id).order_by(Seat.seat_number))
    return [{"id": s.id, "seat_number": s.seat_number, "is_booked": s.is_booked} for s in result.all()]
