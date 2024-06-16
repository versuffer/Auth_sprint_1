from app.exceptions import UserNotFoundError, WrongPasswordError
from app.schemas.api.v1.auth_schemas import ResetUsernameSchema, UserNewSchema, ResetPasswordSchema
from app.services.auth.user_service import UserService
from app.services.utils.password_service import password_service


class UserChangesService:
    def __init__(self):
        self.user_service = UserService()
        self.password_service = password_service

    async def reset_username(self, reset_schema: ResetUsernameSchema) -> UserNewSchema:
        user = await self.user_service.get_user(reset_schema.login)
        if not user:
            raise UserNotFoundError
        return await self.user_service.set_username(user.id, reset_schema.new_username)

    async def reset_password(self, reset_schema: ResetPasswordSchema) -> UserNewSchema:
        user = await self.user_service.get_user(reset_schema.login)
        if not user:
            raise UserNotFoundError
        if not self.password_service.verify_password(user.hashed_password, reset_schema.current_password):
            raise WrongPasswordError
        new_hashed_password = self.password_service.hash_password(reset_schema.new_password)
        return await self.user_service.set_password(user.id, new_hashed_password)

