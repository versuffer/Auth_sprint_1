class UserAlreadyExistError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class WrongPasswordError(Exception):
    pass


class RefreshTokenValidationError(Exception):
    pass
