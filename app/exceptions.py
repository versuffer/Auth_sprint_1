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


class RoleAlreadyExistError(BaseError):
    pass
