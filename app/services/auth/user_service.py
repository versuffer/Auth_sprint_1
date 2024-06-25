import uuid

from app.exceptions import UserAlreadyExistsError
from app.schemas.api.v1.auth_schemas import (
    CreateUserCredentialsSchema,
    HistorySchemaCreate,
    UserNewSchema,
)
from app.schemas.services.auth.user_service_schemas import UserCreateSchema, UserSchema
from app.schemas.services.repositories.history_repository_schemas import HistoryDBSchema
from app.schemas.services.repositories.user_repository_schemas import UserDBSchema
from app.services.repositories.history_repository import history_repository
from app.services.repositories.user_repository import user_repository


class UserService:
    def __init__(self):
        self.user_repository = user_repository
        self.history_repository = history_repository

    async def create(self, user_data: UserCreateSchema) -> UserSchema:
        try:
            user_db_schema = await self.user_repository.create(user_data)
            return UserSchema(**user_db_schema.model_dump())
        except UserAlreadyExistsError as err:
            raise err

    async def get_user(self, login: str) -> UserDBSchema | None:
        return await self.user_repository.get_user_by_login(login)

    async def get_user_by_credentials(self, user_credentials: CreateUserCredentialsSchema) -> UserDBSchema | None:
        return await self.user_repository.get_user_by_credentials(
            email=user_credentials.email, username=user_credentials.username
        )

    async def save_login_history(self, history_data: HistorySchemaCreate) -> None:
        await self.history_repository.create(history_data)

    async def get_history(self, user: UserDBSchema) -> list[HistoryDBSchema]:
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


user_service = UserService()
