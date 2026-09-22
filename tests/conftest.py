import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession
from core.settings import settings

from django.conf import settings as django_settings

if not django_settings.configured:
    django_settings.configure(
        PASSWORD_HASHERS=[
            "django.contrib.auth.hashers.Argon2PasswordHasher",
        ]
    )


@pytest_asyncio.fixture(scope="function")
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))

    await engine.dispose()
