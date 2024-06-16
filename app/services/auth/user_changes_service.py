from app.exceptions import UserNotFoundError
from app.schemas.api.v1.auth_schemas import ResetUsernameSchema, UserNewSchema
from app.services.auth.user_service import UserService


class UserChangesService:
    def __init__(self):
        self.user_service = UserService()

    async def reset_username(self, reset_schema: ResetUsernameSchema) -> UserNewSchema:
        user = await self.user_service.get_user(reset_schema.login)
        if not user:
            raise UserNotFoundError
        return await self.user_service.reset_username(reset_schema.login, reset_schema.new_username)

