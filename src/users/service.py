from typing import Sequence

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.exceptions import EmailAlreadyExistsError, UserNotFoundException, InvalidCredentialsError, \
    UserInactiveError
from src.users.models import User
from src.users.repository import UserRepository
from src.users.schemas import UserCreateSchema, UserUpdateSchema, PaginationParams, UserLoginSchema
from src.users.security import hash_password, verify_password


class UserService:
    def __init__(self, repository: UserRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create(self, data: UserCreateSchema) -> User:
        existing = await self.repository.get_user_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsError()

        payload = data.model_dump()
        raw_password = payload.pop("password")
        payload["password_hash"] = hash_password(raw_password)

        user = User(**payload)
        user = await self.repository.add(user)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all(self, pagination: PaginationParams) -> Sequence[User]:
        result = await self.repository.get_all(limit=pagination.limit, offset=pagination.offset)
        return result

    async def update(self, user_id: UUID4, data: UserUpdateSchema) -> User:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)

        if data.username is not None:
            user.username = data.username
        if data.email is not None:
            user.email = data.email
        if data.age is not None:
            user.age = data.age

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID4) -> None:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)

        await self.repository.delete(user)
        await self.session.commit()

    async def authenticate(self, data: UserLoginSchema) -> User:
        user = await self.repository.get_user_by_email(data.email)
        if not user:
            raise InvalidCredentialsError()

        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise UserInactiveError()

        return user

