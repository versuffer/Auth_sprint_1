from app.exceptions import UserAlreadyExistError
from app.schemas.api.v1.auth_schemas import UserCredentialsSchema, UserNewSchema
from app.schemas.services.auth.user_service_schemas import UserCreatedSchema
from app.services.auth.user_service import UserService
from app.services.utils.hash_service import HashService


class RegistrationService:
    def __init__(self):
        self.hash_service = HashService()
        self.user_service = UserService()

    async def create_user(self, user_credentials: UserCredentialsSchema) -> UserCreatedSchema:
        if await self.user_service.is_user_exist(user_credentials.login):
            raise UserAlreadyExistError
        hashed_data = await self.hash_service.get_hashed_registration_data(user_credentials.password)
        return await self.user_service.create(
            UserNewSchema(
                login=user_credentials.login, password=hashed_data.password, dynamic_salt=hashed_data.dynamic_salt
            )
        )
