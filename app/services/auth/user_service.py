import uuid

from app.exceptions import UserAlreadyExistsError
from app.schemas.api.v1.auth_schemas import (
    HistorySchema,
    HistorySchemaCreate,
    UserHistoryResponseSchema,
    UserNewSchema,
)
from app.schemas.services.auth.user_service_schemas import UserCreateSchema, UserSchema
from app.schemas.services.repositories.user_repository_schemas import UserDBSchema
from app.services.repositories.history_repository import HistoryRepository
from app.services.repositories.user_repository import UserRepository

# class HistoryRepository:
#     async def create(self, history_data: HistorySchema) -> None:
#         pass
#
#     async def get(self, user_id: uuid.UUID) -> UserHistoryResponseSchema:
#         pass


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.history_repository = HistoryRepository()

    async def create(self, user_data: UserCreateSchema) -> UserSchema:
        try:
            user_db_schema = await self.user_repository.create(user_data)
            return UserSchema(**user_db_schema.model_dump())
        except UserAlreadyExistsError as err:
            raise err

    async def get_user(self, login: str) -> UserDBSchema | None:
        return await self.user_repository.get_user_by_login(login)

    async def save_login_history(self, history_data: HistorySchemaCreate) -> None:
        await self.history_repository.create(history_data)

    async def get_history(self, user: UserDBSchema) -> UserHistoryResponseSchema:
        return await self.history_repository.get(user)

    async def check_is_superuser(self, login: str) -> bool:
        user = await self.user_repository.get_user_by_login(login)
        return user.is_superuser

    async def set_username(self, user_id: uuid.UUID, new_username: str) -> UserNewSchema:
        user = await self.user_repository.update(user_id, {'login': new_username})
        return UserNewSchema(login=user.login, hashed_password=user.hashed_password)

    async def set_password(self, user_id: uuid.UUID, new_password: str) -> UserNewSchema:
        user = await self.user_repository.update(user_id, {'hashed_password': new_password})
        return UserNewSchema(login=user.login, hashed_password=user.hashed_password)
