import datetime

from app.exceptions import WrongPasswordError, UserNotFoundError
from app.schemas.api.v1.auth_schemas import UserLoginCredentialsSchema, UserTokensCredentialsSchema, UserTokensSchema, \
    HistorySchema, UserRefreshCredentialsSchema
from app.schemas.services.auth.user_service_schemas import UserDBSchema
from app.services.auth.token_service import TokenService
from app.services.auth.user_service import UserService
from app.services.utils.hash_service import HashService


class AuthenticationService:
    def __init__(self):
        self.hash_service = HashService()
        self.user_service = UserService()
        self.token_service = TokenService()
        self.user: UserDBSchema | None = None

    async def get_tokens_by_login(self, user_credentials: UserLoginCredentialsSchema) -> UserTokensSchema:
        user = await self.user_service.get_user(user_credentials.login)
        if not user:
            raise UserNotFoundError
        hashed_password = await self.hash_service.get_hashed_password(user_credentials.password, user.dynamic_salt)
        if hashed_password != user.hashed_password:
            raise WrongPasswordError
        tokens = await self.token_service.get_tokens(UserTokensCredentialsSchema(login=user.login, roles=user.roles))
        await self.user_service.save_history(
            HistorySchema(id=user.id, auth_date=datetime.datetime.utcnow(), user_agent=user_credentials.user_agent)
        )  # TODO сделать фоновой таской
        return tokens

    async def get_tokens_by_refresh_token(self, user_credentials: UserRefreshCredentialsSchema) -> UserTokensSchema:
        login = await self.token_service.get_login_from_token(user_credentials.refresh_token)
        user = await self.user_service.get_user(login)
        if not user:
            raise UserNotFoundError
        tokens = await self.token_service.get_tokens(UserTokensCredentialsSchema(login=login, roles=user.roles))
        await self.user_service.save_history(
            HistorySchema(id=user.id, auth_date=datetime.datetime.utcnow(), user_agent=user_credentials.user_agent)
        )  # TODO сделать фоновой таской
        return tokens

    async def logout(self, access_token: str) -> None:
        return await self.token_service.delete_session(access_token)

    async def check_access_token(self, access_token: str) -> bool:
        return await self.token_service.check_access_token(access_token)
