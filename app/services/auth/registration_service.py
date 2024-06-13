from app.exceptions import UserAlreadyExistError
from app.schemas.api.v1.auth_schemas import UserCredentialsSchema, UserNewSchema
from app.schemas.services.auth.user_service_schemas import UserCreatedSchema
from app.services.auth.user_service import UserService
from app.services.utils.password_service import password_service


class RegistrationService:
    def __init__(self):
        self.password_service = password_service
        self.user_service = UserService()

    async def create_user(self, user_credentials: UserCredentialsSchema) -> UserCreatedSchema:
        if await self.user_service.is_user_exist(user_credentials.login):
            raise UserAlreadyExistError
        hashed_password = self.password_service.hash_password(user_credentials.password)
        return await self.user_service.create(
            UserNewSchema(login=user_credentials.login, hashed_password=hashed_password)
        )
