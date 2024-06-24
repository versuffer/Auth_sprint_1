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


class RefreshTokenValidationError(BaseError):
    pass


class AccessTokenValidationError(BaseError):
    pass


class RoleAlreadyExistError(BaseError):
    pass
