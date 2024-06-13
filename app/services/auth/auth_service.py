import datetime

from app.exceptions import UserNotFoundError, WrongPasswordError
from app.schemas.api.v1.auth_schemas import (
    CredentialsLoginDataSchema,
    HistorySchema,
    RefreshLoginDataSchema,
    UserTokenDataSchema,
    UserTokensSchema,
)
from app.schemas.services.auth.user_service_schemas import UserDBSchema
from app.services.auth.session_service import SessionService
from app.services.auth.user_service import UserService
from app.services.utils.password_service import password_service


class AuthenticationService:
    def __init__(self):
        self.password_service = password_service
        self.user_service = UserService()
        self.session_service = SessionService()
        self.user: UserDBSchema | None = None

    async def _get_user(self, login: str) -> UserDBSchema:
        if user := await self.user_service.get_user(login):
            return user
        raise UserNotFoundError

    def _verify_user_password(self, user: UserDBSchema, password: str):
        if not self.password_service.verify_password(user.hashed_password, password):
            raise WrongPasswordError

    async def _get_auth_token_pair(self, user: UserDBSchema) -> UserTokensSchema:
        return await self.session_service.create_token_pair(UserTokenDataSchema(login=user.login, roles=user.roles))

    async def _save_user_login_history(
        self, user: UserDBSchema, login_data: CredentialsLoginDataSchema | RefreshLoginDataSchema
    ):
        await self.user_service.save_login_history(
            HistorySchema(id=user.id, auth_date=datetime.datetime.utcnow(), user_agent=login_data.user_agent)
        )  # TODO сделать фоновой таской

    async def authenticate_by_credentials(self, login_data: CredentialsLoginDataSchema) -> UserTokensSchema:
        user = await self._get_user(login=login_data.login)
        self._verify_user_password(user=user, password=password_service)
        tokens = await self._get_auth_token_pair(user=user)
        await self._save_user_login_history(user=user, login_data=login_data)
        return tokens

    async def authenticate_by_refresh_token(self, login_data: RefreshLoginDataSchema) -> UserTokensSchema:
        login = await self.session_service.get_login_from_refresh_token(refresh_token=login_data.refresh_token)
        user = await self._get_user(login=login)
        tokens = await self._get_auth_token_pair(user=user)
        await self._save_user_login_history(user=user, login_data=login_data)
        return tokens

    async def logout(self, access_token: str) -> str:
        return await self.session_service.delete_session(access_token)

    async def verify_access_token(self, access_token: str) -> bool:
        return self.session_service.verify_access_token(access_token)
