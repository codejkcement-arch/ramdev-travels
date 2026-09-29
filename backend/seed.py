import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal, init_db
from app.models.user import User
from app.models.bus import Bus, Seat
from app.models.flight import Flight
from app.models.cinema import Cinema, CinemaShow, CinemaSeat
from app.utils.security import hash_password
from datetime import datetime, timedelta

async def main():
    from app.config import settings
    if not settings.ADMIN_EMAIL or not settings.ADMIN_PASSWORD:
        raise RuntimeError("Set ADMIN_EMAIL and ADMIN_PASSWORD before seeding")
    if settings.ENVIRONMENT.lower() == "production":
        raise RuntimeError("Do not run seed.py in production")
    await init_db()
    async with AsyncSessionLocal() as db:
        if not await db.scalar(select(User).where(User.email == settings.ADMIN_EMAIL)):
            db.add(User(name="Admin", email=settings.ADMIN_EMAIL,
                        password_hash=hash_password(settings.ADMIN_PASSWORD), is_admin=True))
        if not await db.scalar(select(Bus).where(Bus.bus_number == "RDT001")):
            bus = Bus(operator="Ramdev Travels", bus_number="RDT001",
                      source="Jodhpur", destination="Jaipur",
                      departure_time="22:00", arrival_time="05:30", fare=650, total_seats=40)
            db.add(bus)
            await db.flush()
            for i in range(1, 41):
                db.add(Seat(bus_id=bus.id, seat_number=f"{(i+1)//2}{'L' if i%2 else 'R'}"))
        if not await db.scalar(select(Flight).where(Flight.flight_number == "RDT100")):
            db.add(Flight(airline="Ramdev Air Demo", flight_number="RDT100",
                          source="Jodhpur", destination="Delhi",
                          departure_time=datetime.now()+timedelta(days=1),
                          arrival_time=datetime.now()+timedelta(days=1, hours=2),
                          fare=4500, available_seats=180))
        if not await db.scalar(select(Cinema).where(Cinema.name == "Ramdev Cinema")):
            cinema = Cinema(name="Ramdev Cinema", city="Jodhpur", address="Main Road")
            db.add(cinema)
            await db.flush()
            show = CinemaShow(cinema_id=cinema.id, movie_name="Demo Movie",
                              show_time=datetime.now()+timedelta(hours=4), price=180, total_seats=50)
            db.add(show)
            await db.flush()
            for i in range(1, 51):
                db.add(CinemaSeat(show_id=show.id, seat_number=f"A{i}"))
        await db.commit()
    print("Seed complete")

if __name__ == "__main__":
    asyncio.run(main())
