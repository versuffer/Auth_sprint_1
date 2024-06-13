from app.schemas.api.v1.auth_schemas import HistorySchema, UserNewSchema
from app.schemas.services.auth.user_service_schemas import (
    UserCreatedSchema,
    UserDBSchema,
)


class UserRepository:
    async def get_user_by_login(self, login: str) -> UserDBSchema:
        pass

    async def create(self, user_data: UserNewSchema) -> UserDBSchema:
        pass


class HistoryRepository:
    async def create(self, history_data: HistorySchema) -> None:
        pass


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.history_repository = HistoryRepository()

    async def is_user_exist(self, login) -> bool:
        if await self.user_repository.get_user_by_login(login):
            return True
        return False

    async def create(self, user_data: UserNewSchema) -> UserCreatedSchema:
        user_db = await self.user_repository.create(user_data)
        return UserCreatedSchema(id=user_db.id, login=user_db.login, is_superuser=user_db.is_superuser)

    async def get_user(self, login: str) -> UserDBSchema:
        return await self.user_repository.get_user_by_login(login)

    async def save_history(self, history_data: HistorySchema) -> None:
        await self.history_repository.create(history_data)

    async def check_is_superuser(self, login: str) -> bool:
        user = await self.user_repository.get_user_by_login(login)
        return user.is_superuser
