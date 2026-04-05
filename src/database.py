from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from src.config import settings

# Асинхронный движок — для основного приложения (FastAPI + async/await)
async_engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DEBUG,  # Если DEBUG=True, будет логировать SQL-запросы в консоль
)

# Синхронный движок — для миграций Alembic и скриптов
sync_engine = create_engine(
    str(settings.DATABASE_URL).replace("+asyncpg", ""),  # Убираем "+asyncpg" для обычного psycopg2
    echo=settings.DEBUG,
)


# ============================================
# ФАБРИКА СЕССИЙ
# ============================================

# Создаёт асинхронные сессии для работы с БД
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,        # Явно указываем тип сессии
    expire_on_commit=False,     # После commit() объекты не будут "протухать"
    autocommit=False,           # Не коммитить автоматически
    autoflush=False,            # Не делать flush перед каждым запросом
)

# Синхронная фабрика сессий (для миграций)
SyncSessionLocal = sessionmaker(
    sync_engine,
    class_=Session,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    Базовый класс для всех SQLAlchemy моделей.
    """
    pass


async def get_async_session():
    """
    Зависимость для dependency injection в FastAPI.
    
    Использование в роутах:
        @app.get("/users")
        async def get_users(session: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def setup_database():
    """
    Создаёт все таблицы в БД на основе моделей.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
