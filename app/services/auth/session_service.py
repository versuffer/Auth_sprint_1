import uuid
from datetime import datetime

from app.core.config import app_settings
from app.db.redis.redis_repo import RedisRepository
from app.exceptions import RefreshTokenValidationError
from app.schemas.api.v1.auth_schemas import UserTokenDataSchema, UserTokensSchema
from app.services.utils.jwt_service import jwt_service


class SessionService:
    def __init__(self):
        self.jwt_service = jwt_service
        self.redis_repo = RedisRepository(app_settings.REDIS_DSN)

    async def create_token_pair(self, user_token_data: UserTokenDataSchema) -> UserTokensSchema:
        user_login = user_token_data.login
        session_id = uuid.uuid4()
        base_expire_time = datetime.utcnow()
        base_token_payload = {'session_id': str(session_id)}

        access_token_payload = user_token_data.model_dump()
        access_token_payload |= base_token_payload
        access_token = self.jwt_service.create_access_token(
            payload=access_token_payload, base_expire_time=base_expire_time
        )

        refresh_token_payload = {'login': user_login}
        refresh_token_payload |= base_token_payload
        refresh_token = self.jwt_service.create_refresh_token(
            payload=refresh_token_payload, base_expire_time=base_expire_time
        )

        await self.redis_repo.save_session(user_login, session_id=session_id)
        return UserTokensSchema(access_token=access_token, refresh_token=refresh_token)

    async def get_login_from_refresh_token(self, refresh_token: str) -> str | None:
        token_payload = self.jwt_service.get_token_payload(token=refresh_token)
        if token_payload and token_payload.get('refresh') is True:
            if login := token_payload.get('login'):
                return login

            raise RefreshTokenValidationError

        # TODO вместо return None нужно рейзить кастомную ошибку
        return None

    def verify_access_token(self, access_token: str) -> bool:
        token_payload = self.jwt_service.get_token_payload(token=access_token)
        if token_payload and 'refresh' not in token_payload:
            return True
        return False

    async def delete_session(self, access_token: str) -> str:
        token_payload = self.jwt_service.get_token_payload(token=access_token, verify_exp=False)
        if session_id := token_payload.get('session_id'):
            await self.redis_repo.delete_session(session_id)

        return session_id
