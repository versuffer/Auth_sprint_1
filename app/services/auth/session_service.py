import uuid

from app.core.config import app_settings
from app.db.redis.redis_repo import RedisRepository
from app.schemas.api.v1.auth_schemas import (
    UserTokensCredentialsSchema,
    UserTokensSchema,
)


class JWTService:
    async def get_tokens(
        self, user_credentials: UserTokensCredentialsSchema, session_id: uuid.UUID
    ) -> UserTokensSchema:
        pass

    async def get_login(self, token: str) -> str:
        pass

    async def get_session_id(self, token: str) -> uuid.UUID:
        pass

    async def check_token(self, token: str) -> bool:
        pass


class SessionsService:
    def __init__(self):
        self.jwt_service = JWTService()
        self.redis_repo = RedisRepository(app_settings.REDIS_DSN)

    async def get_tokens(self, user_credentials: UserTokensCredentialsSchema) -> UserTokensSchema:
        session_id = uuid.uuid4()
        tokens = await self.jwt_service.get_tokens(user_credentials, session_id)
        await self.redis_repo.save_session(user_credentials.login, session_id=session_id)
        return tokens

    async def get_login_from_token(self, token: str) -> str:
        return await self.jwt_service.get_login(token)

    async def delete_session(self, access_token: str) -> None:
        session_id = await self.jwt_service.get_session_id(access_token)
        await self.redis_repo.delete_session(session_id)
        return None

    async def check_access_token(self, access_token: str) -> bool:
        is_token_valid = await self.jwt_service.check_token(access_token)
        if not is_token_valid:
            return False
        session_id = await self.jwt_service.get_session_id(access_token)
        if not session_id:
            return False
        return True
