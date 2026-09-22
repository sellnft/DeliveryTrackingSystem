import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from repository.userRepository import UserRepository
from services.userService import UserService
from models.user import UserRole, User
from models.order import Order

pytestmark = pytest.mark.asyncio


async def test_successful_registration_and_login(test_session: AsyncSession):
    repo = UserRepository(test_session)
    service = UserService(repo)

    new_user = await service.register_user(
        username="test_courier",
        password_raw="super_secret_123",
        full_name="Иван Курьеров",
        phone="+79991112233",
        role=UserRole.COURIER
    )

    assert new_user.id is not None
    assert new_user.username == "test_courier"
    assert new_user.role == UserRole.COURIER

    logged_user_by_name = await service.login_user(
        login_value="test_courier",
        password_raw="super_secret_123"
    )
    assert logged_user_by_name.id == new_user.id

    logged_user_by_phone = await service.login_user(
        login_value="+79991112233",
        password_raw="super_secret_123"
    )
    assert logged_user_by_phone.id == new_user.id


async def test_login_with_wrong_password(test_session: AsyncSession):

    repo = UserRepository(test_session)
    service = UserService(repo)

    await service.register_user(
        username="client1",
        password_raw="correct_pass",
        full_name="Клиент Обычный",
        phone="+79990000000"
    )

    with pytest.raises(ValueError) as exc_info:
        await service.login_user(login_value="client1",
                                 password_raw="wrong_pass")

    assert "Неверное имя пользователя/телефон или пароль" in str(
        exc_info.value)


# tests/test_user_service.py
# ... ваш существующий код импортов и первых двух тестов ...

async def test_registration_with_existing_username_or_phone(
        test_session: AsyncSession):
    repo = UserRepository(test_session)
    service = UserService(repo)

    await service.register_user(
        username="original_user",
        password_raw="password123",
        full_name="Оригинальный Пользователь",
        phone="+79991112233"
    )

    with pytest.raises(ValueError) as exc_info_username:
        await service.register_user(
            username="original_user",
            password_raw="different_pass",
            full_name="Иван Иванов",
            phone="+79994445566"
        )

    assert "Пользователь с таким username уже существует" in str(
        exc_info_username.value)

    with pytest.raises(ValueError) as exc_info_phone:
        await service.register_user(
            username="new_unique_user",
            password_raw="different_pass",
            full_name="Петр Петров",
            phone="+79991112233"
        )

    assert "Пользователь с таким номером телефона уже зарегистрирован" in str(
        exc_info_phone.value)
