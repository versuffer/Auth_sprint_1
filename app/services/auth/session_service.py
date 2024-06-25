import uuid
from datetime import datetime

from jwt import InvalidTokenError

from app.db.redis.redis_repo import redis_repo
from app.exceptions import (
    AccessTokenValidationError,
    ExpiredSessionError,
    RefreshTokenValidationError,
    TokenDoesNotContainLogin,
)
from app.schemas.api.v1.auth_schemas import SessionDataSchema, UserTokenDataSchema
from app.services.utils.jwt_service import jwt_service


class SessionService:
    def __init__(self):
        self.jwt_service = jwt_service
        self.redis_repo = redis_repo

    async def create_session(self, user_token_data: UserTokenDataSchema) -> SessionDataSchema:
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
        return SessionDataSchema(access_token=access_token, refresh_token=refresh_token, session_id=session_id)

    async def get_login_from_refresh_token(self, refresh_token: str) -> str:
        try:
            token_payload = self.jwt_service.get_token_payload(token=refresh_token)
        except InvalidTokenError:
            raise RefreshTokenValidationError

        if not token_payload.get('refresh') is True:
            raise RefreshTokenValidationError

        if not (session_id := token_payload.get('session_id')):
            raise RefreshTokenValidationError

        if not await self.redis_repo.get_session(session_id):
            raise ExpiredSessionError

        if not (login := token_payload.get('login')):
            raise TokenDoesNotContainLogin

        return login

    async def get_login_from_access_token(self, access_token: str) -> str | None:
        token_payload = self.jwt_service.get_token_payload(token=access_token)
        if token_payload:
            try:
                refresh_mark = token_payload['refresh']  # noqa
                raise AccessTokenValidationError
            except KeyError:
                if login := token_payload.get('login'):
                    return login

        # TODO вместо return None нужно рейзить кастомную ошибку
        return None

    def verify_access_token(self, access_token: str) -> bool:
        token_payload = self.jwt_service.get_token_payload(token=access_token)
        if token_payload and 'refresh' not in token_payload:
            return True
        return False

    async def delete_session(self, token: str) -> str:
        token_payload = self.jwt_service.get_token_payload(token=token, verify_exp=False)
        if session_id := token_payload.get('session_id'):
            await self.redis_repo.delete_session(session_id)

        return session_id
