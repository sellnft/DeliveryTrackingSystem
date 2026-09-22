from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession

from core.settings import settings


class DatabaseManager:
    def __init__(self, db_url: str, echo: bool = False):
        self.engine = create_async_engine(
            db_url,
            echo=echo,
            pool_size=10,
            max_overflow=20
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


db_manager = DatabaseManager(db_url=settings.get_db_url(), echo=False)
