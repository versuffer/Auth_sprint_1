from fastapi import HTTPException
from starlette import status


class BaseError(Exception):
    message: str = 'Base Error'

    def __init__(self, *args: object, message: str | None = None) -> None:
        self.message = message or self.message
        if args:
            self.message += f' Details: {self.args}'
        super().__init__(*args)


class UserAlreadyExistsError(BaseError):
    pass


class UserNotFoundError(BaseError):
    pass


class RoleNotFoundError(BaseError):
    pass


class WrongPasswordError(BaseError):
    pass


class TokenError(BaseError):
    pass


class TokenValidationError(TokenError):
    pass


class RefreshTokenValidationError(TokenValidationError):
    pass


class AccessTokenValidationError(TokenValidationError):
    pass


class TokenDoesNotContainSessionId(TokenError):
    pass


class TokenDoesNotContainLogin(TokenError):
    pass


class ExpiredSessionError(TokenError):
    pass


class RoleAlreadyExistsError(BaseError):
    pass


class AuthorizationError(BaseError):
    pass


auth_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
not_found_error = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
user_not_found_error = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
user_already_exists_error = HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
role_already_exists_error = HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Role already exists')
