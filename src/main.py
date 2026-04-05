from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import async_engine
from src.users.router import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # При запуске
    print("🚀 Приложение запускается...")
    yield
    # При выключении
    print("🛑 Приложение останавливается...")
    await async_engine.dispose()


app = FastAPI(
    title="Study FastAPI",
    description="Учебный проект по FastAPI Best Practices",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/", summary="Главная ручка", tags=["Основные ручки"])
async def root():
    return {"message": "Hello World"}

app.include_router(users_router)