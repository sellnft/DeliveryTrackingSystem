from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user) 
        return user

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_login_or_phone(self, login_value: str) -> User | None:
        query = select(User).where(
            or_(
                User.username == login_value,
                User.phone == login_value
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
