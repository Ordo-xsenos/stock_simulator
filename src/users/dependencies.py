import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.exceptions import UserNotFoundException, UserInactiveError
from src.users.models import User
from src.users.repository import UserRepository
from src.users.schemas import PaginationParams
from src.database import get_async_session
from src.users.security import decode_access_token
from src.users.service import UserService


# Указываем FastAPI, где искать токен для аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

# --- Фабрики для сервисов и репозиториев ---

async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

async def get_user_service(repository: UserRepositoryDep, session: SessionDep) -> UserService:
    return UserService(repository, session)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

# --- Утилитарные зависимости ---

async def get_pagination_params(limit: int = 100, offset: int = 0) -> PaginationParams:
    """Создаёт параметры пагинации из query параметров."""
    return PaginationParams(limit=limit, offset=offset)

PaginationDep = Annotated[PaginationParams, Depends(get_pagination_params)]

# Получение текущего пользователя из токена

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], # Получаем токен из заголовка Authorization
        repository: UserRepositoryDep
) -> User:
    data = decode_access_token(token)
    user_id = uuid.UUID(data["sub"])
    user = await repository.get_user_by_id(user_id)
    if user is None:
        raise UserNotFoundException(user_id)
    if not user.is_active:
        raise UserInactiveError()

    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]
