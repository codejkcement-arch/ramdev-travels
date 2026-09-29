from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from app.config import settings

# NullPool works well with Supabase's shared pooler and keeps the API from
# opening a large application-side connection pool on a free hosted service.
connect_args = {"statement_cache_size": 0} if settings.DATABASE_URL.startswith("postgresql+asyncpg://") else {}
engine = create_async_engine(settings.DATABASE_URL, echo=False, poolclass=NullPool, connect_args=connect_args)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    from app.models import user, booking, bus, flight, cinema, payment, refund
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
