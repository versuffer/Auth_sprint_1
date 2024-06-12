from app.schemas.api.v1.auth_schemas import HistorySchema
from app.schemas.services.auth.user_service_schemas import (
    UserCreatedSchema,
    UserDBSchema,
)


class UserService:
    async def is_user_exist(self, login) -> bool:
        pass

    async def create(self, hashed_password, dynamic_salt) -> UserCreatedSchema:
        pass

    async def get_user(self, login: str) -> UserDBSchema:
        pass

    async def save_history(self, history_data: HistorySchema) -> None:
        pass
