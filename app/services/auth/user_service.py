from app.schemas.services.auth.user_service_schemas import UserCreatedSchema


class UserService:
    async def is_user_exist(self, login) -> bool:
        pass

    async def create(self, hashed_password, dynamic_salt) -> UserCreatedSchema:
        pass
