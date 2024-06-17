import re
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logs import logger
from app.db.postgres.models.users import UserModel, UserRoleAssociationModel
from app.exceptions import UserAlreadyExist
from app.schemas.api.v1.auth_schemas import UserNewSchema
from app.schemas.services.auth.user_service_schemas import UserDBSchema
from app.services.repositories.postgres_repository import PostgresService


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db: PostgresService = PostgresService(session)

    def _get_login_type(self, login: str):
        """Метод проверяет что передано в качестве логина email или username и возвращает необходимое поле для поиска"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, login):
            return UserModel.email
        return UserModel.username

    async def get_user_by_login(self, login: str) -> UserDBSchema:
        """Возвращает пользователя и сама определяет тип логина email или username"""

        db_user = await self.db.get_one_obj(
            UserModel, where_value=[(self._get_login_type(login), login)], select_in_load=UserModel.roles
        )
        return UserDBSchema.model_validate(db_user) if db_user else None

    async def get(self, user_id: UUID) -> UserDBSchema | None:
        db_user = await self.db.get_one_obj(
            UserModel, where_value=[(UserModel.id, user_id)], select_in_load=UserModel.roles
        )
        return UserDBSchema.model_validate(db_user) if db_user else None

    async def create(self, user_data: UserNewSchema) -> UserDBSchema | None:
        try:
            user = UserModel(**user_data.model_dump(exclude_none=True))
            await self.db.create_obj(user)
            return await self.get(user.id)
        except IntegrityError:
            logger.error(UserAlreadyExist('User already exist'))
            return None

    async def update(self, user_id: UUID, data: dict) -> UserDBSchema | None:
        try:
            await self.db.update_obj(UserModel, where_value=[(UserModel.id, user_id)], update_values=data)
            return await self.get(user_id)
        except IntegrityError:
            logger.error(UserAlreadyExist('User already exist'))
            return None

    async def add_user_role(self, user_id: UUID, role_id: UUID) -> UserDBSchema | None:
        try:
            user_role = UserRoleAssociationModel(user_id=user_id, role_id=role_id)
            await self.db.create_obj(user_role)
            return await self.get(user_id)
        except IntegrityError as err:
            logger.error('user_id=%s already exist role_id=%s. Error=%s', user_id, role_id, err)
            return None

    async def delete_user_role(self, user_id: UUID, role_id: UUID) -> UserDBSchema | None:

        try:
            await self.db.delete_obj(
                UserRoleAssociationModel,
                where_value=[(UserRoleAssociationModel.user_id, user_id), (UserRoleAssociationModel.role_id, role_id)],
            )
            await self.get(user_id)
        except Exception as err:
            logger.error('Can not delete role_id=%s error=%s', role_id, err)
            return None
