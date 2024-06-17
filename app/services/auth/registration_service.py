from app.exceptions import UserAlreadyExistsError
from app.schemas.api.v1.auth_schemas import RegisterUserCredentialsSchema
from app.schemas.services.auth.user_service_schemas import UserCreateSchema, UserSchema
from app.services.auth.user_service import UserService
from app.services.utils.password_service import password_service


class RegistrationService:
    def __init__(self):
        self.password_service = password_service
        self.user_service = UserService()

    async def create_user(self, user_credentials: RegisterUserCredentialsSchema) -> UserSchema:
        try:
            hashed_password = self.password_service.hash_password(user_credentials.password)
            return await self.user_service.create(
                UserCreateSchema(**user_credentials.model_dump(), hashed_password=hashed_password)
            )
        except UserAlreadyExistsError as err:
            raise err
