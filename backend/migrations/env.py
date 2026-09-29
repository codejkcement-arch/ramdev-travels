from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from app.database import Base
from app.models import *
from app.config import settings
import asyncio

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=settings.DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(lambda c: context.configure(connection=c, target_metadata=target_metadata))
        async with connection.begin():
            await connection.run_sync(lambda c: context.run_migrations())
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
