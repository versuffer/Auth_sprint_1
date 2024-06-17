class UserAlreadyExistError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class RoleNotFoundError(Exception):
    pass


class WrongPasswordError(Exception):
    pass


class RefreshTokenValidationError(Exception):
    pass


class RoleAlreadyExist(Exception):
    pass


class UserAlreadyExist(Exception):
    pass
