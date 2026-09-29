from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database import get_db
from app.models.flight import Flight
from app.services.booking_service import expire_booking_holds

router = APIRouter()

@router.get("/search")
async def search(source: str, destination: str, db: AsyncSession = Depends(get_db)):
    await expire_booking_holds(db)
    await db.commit()
    result = await db.scalars(select(Flight).where(
        and_(Flight.source.ilike(f"%{source}%"), Flight.destination.ilike(f"%{destination}%"))
    ))
    return [{"id": f.id, "airline": f.airline, "flight_number": f.flight_number,
             "source": f.source, "destination": f.destination,
             "departure_time": f.departure_time, "arrival_time": f.arrival_time,
             "fare": f.fare, "available_seats": f.available_seats} for f in result.all()]
