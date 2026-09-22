from utils.hashPassword import hash_password
from utils.checkPassword import verify_password
from repository.userRepository import UserRepository
from models.user import User, UserRole


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(
        self,
        username: str,
        password_raw: str,
        full_name: str,
        phone: str,
        email: str | None = None,
        role: UserRole = UserRole.CLIENT
    ) -> User:
        if await self.user_repo.get_by_username(username):
            raise ValueError("Пользователь с таким username уже существует")

        if await self.user_repo.get_by_login_or_phone(phone):
            raise ValueError(
                "Пользователь с таким номером телефона уже зарегистрирован")

        hashed_password = hash_password(password_raw)

        new_user = User(
            username=username,
            password_hash=hashed_password,
            full_name=full_name,
            phone=phone,
            email=email,
            role=role
        )

        return await self.user_repo.add_user(new_user)

    async def login_user(self, login_value: str, password_raw: str) -> User:
        user = await self.user_repo.get_by_login_or_phone(login_value)

        if not user or not user.is_active:
            raise ValueError("Неверное имя пользователя/телефон или пароль")

        is_password_correct = verify_password(password_raw, user.password_hash)

        if not is_password_correct:
            raise ValueError("Неверное имя пользователя/телефон или пароль")

        return user
