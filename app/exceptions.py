class UserAlreadyExistError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class RoleNotFoundError(Exception):
    pass


class WrongPasswordError(Exception):
    pass
