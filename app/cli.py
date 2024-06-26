import asyncio
from functools import wraps

import anyio
import typer
from sqlalchemy.exc import IntegrityError

from app.core.config import app_settings
from app.core.logs import logger

from app.schemas.services.auth.user_service_schemas import SuperUserCreateSchema
from app.services.repositories.user_repository import UserRepository

cli_app = typer.Typer()


def admin_required(func):
    """Проверка прав для выполнения команд."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if app_settings.IS_ADMIN is not True or not app_settings.ADMIN_CLI_PASSWORD:
            print('Permission denied.')
            return
        user_password = typer.prompt('Enter your cli admin password', hide_input=True)
        if not user_password == app_settings.ADMIN_CLI_PASSWORD:
            print('The password is incorrect.')
            return
        return func(*args, **kwargs)
    return wrapper


@cli_app.command("create-superuser")
@admin_required
def create_superuser():
    """Create user in DB or print exception."""
    try:
        user_repository = UserRepository()

        user = SuperUserCreateSchema(
            username=typer.prompt('username').strip(),
            email=typer.prompt('email').strip(),
            hashed_password=typer.prompt('password', hide_input=True),
            is_superuser=True,
        )
        asyncio.run(user_repository.create(user))
        logger.info(f'Admin "{user.username}" successfully created.')
    except IntegrityError:
        print('An admin with this login already exists.')
    except Exception as e:
        print(f'Oops, something went wrong: {e}')


if __name__ == '__main__':
    cli_app()
