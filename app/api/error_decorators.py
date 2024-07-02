import functools

from app.exceptions import (
    AuthorizationError,
    RoleAlreadyAssignedError,
    RoleNotAssignedError,
    RoleNotFoundError,
    TokenError,
    UserNotFoundError,
    auth_error,
    role_already_assigned_error,
    role_not_assigned_error,
    role_not_found_error,
    user_not_found_error,
)


def handle_auth_router_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (TokenError, UserNotFoundError, AuthorizationError):
            raise auth_error
        except UserNotFoundError:
            raise user_not_found_error
        except RoleNotFoundError:
            raise role_not_found_error
        except RoleAlreadyAssignedError:
            raise role_already_assigned_error
        except RoleNotAssignedError:
            raise role_not_assigned_error

    return wrapper
