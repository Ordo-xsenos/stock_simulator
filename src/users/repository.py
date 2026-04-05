from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id):
        return await self.session.get(User, user_id)

    async def add(self, user: User) -> User:
        self.session.add(user)
        return user

    async def get_user_by_email(self, email):
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return  result.scalar_one_or_none()

    async def get_all(self, limit, offset):
        result = await self.session.execute(
            select(User).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def delete(self, user: User):
        await self.session.delete(user)
