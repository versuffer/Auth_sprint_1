from app.schemas.api.v1.auth_schemas import (
    UserTokensCredentialsSchema,
    UserTokensSchema,
)


class TokenService:
    async def get_tokens(self, user_credentials: UserTokensCredentialsSchema) -> UserTokensSchema:
        pass

    async def get_login_from_token(self, token: str) -> str:
        pass

    async def delete_session(self, access_token: str) -> None:
        pass

    async def check_access_token(self, access_token: str) -> bool:
        pass
