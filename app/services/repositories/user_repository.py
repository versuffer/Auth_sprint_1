import re
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logs import logger
from app.db.postgres.base import manage_async_session
from app.db.postgres.models.users import UserModel, UserRoleAssociationModel
from app.exceptions import RoleAlreadyExistError, UserAlreadyExistsError
from app.schemas.services.auth.user_service_schemas import UserCreateSchema
from app.schemas.services.repositories.user_repository_schemas import UserDBSchema
from app.services.repositories.postgres_repository import PostgresRepository


class UserRepository:
    def __init__(self):
        self.db: PostgresRepository = PostgresRepository()

    async def get_user_by_login(self, login: str, *, session: AsyncSession | None = None) -> UserDBSchema | None:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(email_pattern, login) is not None:
            return await self._get_user_by_email(login)
        return await self._get_user_by_username(login)

    async def _get_user_by_email(self, email: EmailStr, *, session: AsyncSession | None = None) -> UserDBSchema | None:
        db_user = await self.db.get_one_obj(
            UserModel, where_value=[(UserModel.email, email)], select_in_load=[UserModel.roles, UserModel.history], session=session
        )
        return UserDBSchema.model_validate(db_user) if db_user else None

    async def _get_user_by_username(self, username: str, *, session: AsyncSession | None = None) -> UserDBSchema | None:
        db_user = await self.db.get_one_obj(
            UserModel, where_value=[(UserModel.username, username)], select_in_load=[UserModel.roles, UserModel.history], session=session
        )
        return UserDBSchema.model_validate(db_user) if db_user else None

    async def get(self, user_id: UUID, *, session: AsyncSession | None = None) -> UserDBSchema | None:
        db_user = await self.db.get_one_obj(
            UserModel, where_value=[(UserModel.id, user_id)], select_in_load=UserModel.roles, session=session
        )
        return UserDBSchema.model_validate(db_user) if db_user else None

    @manage_async_session
    async def create(self, user_data: UserCreateSchema, *, session: AsyncSession | None = None) -> UserDBSchema:
        if user := await self._get_user_by_username(username=user_data.username, session=session):
            raise UserAlreadyExistsError(message=f'User with such username already exists: {user.username}')

        if user := await self._get_user_by_email(email=user_data.email, session=session):
            raise UserAlreadyExistsError(message=f'User with such email already exists: {user.email}')

        user_model = UserModel(**user_data.model_dump())
        await self.db.create_obj(user_model)
        return await self.get(user_model.id, session=session)

    async def update(self, user_id: UUID, data: dict) -> UserDBSchema | None:
        try:
            await self.db.update_obj(UserModel, where_value=[(UserModel.id, user_id)], update_values=data)
            return await self.get(user_id)
        except IntegrityError:
            # logger.error(UserAlreadyExist('User already exist'))
            return None

    async def add_user_role(self, user_id: UUID, role_id: UUID) -> UserDBSchema | None:
        try:
            user_role = UserRoleAssociationModel(user_id=user_id, role_id=role_id)
            await self.db.create_obj(user_role)
            return await self.get(user_id)
        except IntegrityError as err:
            logger.error('user_id=%s already exist role_id=%s. Error=%s', user_id, role_id, err)
            raise RoleAlreadyExistError

    async def delete_user_role(self, user_id: UUID, role_id: UUID) -> UserDBSchema | None:
        try:
            await self.db.delete_obj(
                UserRoleAssociationModel,
                where_value=[(UserRoleAssociationModel.user_id, user_id), (UserRoleAssociationModel.role_id, role_id)],
            )
            return await self.get(user_id)
        except Exception as err:
            logger.error('Can not delete role_id=%s error=%s', role_id, err)
            return None
