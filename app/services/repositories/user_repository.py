import re
from uuid import UUID

from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logs import logger
from app.db.postgres.models.users import UserModel, UserRoleAssociationModel
from app.schemas.api.v1.auth_schemas import UserNewSchema
from app.schemas.services.auth.user_service_schemas import UserDBSchema


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_login_type(self, login: str):
        """Метод проверяет что передано в качестве логина email или username и возвращает необходимое поле для поиска"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, login):
            return UserModel.email
        return UserModel.username

    async def get_user_by_login(self, login: str) -> UserDBSchema:
        """Возвращает пользователя и сама определяет тип логина email или username"""

        query = select(UserModel).where(self.get_login_type(login) == login).options(selectinload(UserModel.roles))
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return UserDBSchema.model_validate(user) if user else None

    async def get(self, user_id: UUID) -> UserDBSchema | None:
        query = select(UserModel).where(UserModel.id == user_id).options(selectinload(UserModel.roles))
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return UserDBSchema.model_validate(user) if user else None

    async def create(self, user_data: UserNewSchema) -> UserDBSchema | None:

        try:
            user = UserModel(**user_data.model_dump(exclude_none=True))
            self.session.add(user)
            await self.session.commit()
        except Exception as err:
            await self.session.rollback()
            logger.error(err)
            return None
        return await self.get(user.id)

    async def update(self, user_id: UUID, data: dict) -> UserDBSchema | None:
        query = update(UserModel).where(UserModel.id == user_id).values(**data)
        try:
            await self.session.execute(query)
            await self.session.commit()
        except Exception as err:
            await self.session.rollback()
            logger.error(err)
            return None
        return await self.get(user_id)

    async def add_user_role(self, user_id: UUID, role_id: UUID) -> UserDBSchema | None:
        try:
            user_role = UserRoleAssociationModel(user_id=user_id, role_id=role_id)
            self.session.add(user_role)
            await self.session.commit()
        except Exception as err:
            await self.session.rollback()
            logger.error(err)
            return None
        return await self.get(user_id)

    async def delete_user_role(self, user_id: UUID, role_id: UUID) -> UserDBSchema | None:
        try:
            query = delete(UserRoleAssociationModel).where(
                and_(UserRoleAssociationModel.user_id == user_id, UserRoleAssociationModel.role_id == role_id)
            )
            await self.session.execute(query)
            await self.session.commit()
        except Exception as err:
            await self.session.rollback()
            logger.error(err)
            return None
        return await self.get(user_id)
