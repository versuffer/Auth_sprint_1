from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logs import logger
from app.db.postgres.models.users import RoleModel, UserRoleAssociationModel
from app.exceptions import RoleAlreadyExist
from app.schemas.api.v1.roles_schemas import RoleSchema
from app.services.repositories.postgres_repository import PostgresService


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.db: PostgresService = PostgresService(session)

    async def _check_exists_role(self, *, role_id: UUID | None = None, role_title: str | None = None) -> bool:
        if not role_id and not role_title:
            raise ValueError("Either 'id' or 'title' must be provided.")

        if role_id:
            return await self.db.get_one_obj(RoleModel, where_value=[(RoleModel.id, role_id)]) is not None

        return await self.db.get_one_obj(RoleModel, where_value=[(RoleModel.title, role_title)]) is not None

    async def get_all(self) -> Sequence[RoleSchema]:
        db_roles = await self.db.get_all_obj(RoleModel)
        return [RoleSchema.model_validate(db_role) for db_role in db_roles]

    async def get(self, role_id: UUID) -> RoleSchema | None:
        db_role = await self.db.get_one_obj(RoleModel, where_value=[(RoleModel.id, role_id)])
        return RoleSchema.model_validate(db_role) if db_role else None

    async def create(self, title: str, description: str) -> RoleSchema | None:
        try:
            role = RoleModel(title=title, description=description)
            await self.db.create_obj(role)
            return await self.get(role.id)
        except IntegrityError:
            logger.error(RoleAlreadyExist('Role already exist'))
            return None

    async def update(self, role_id: UUID, data: dict) -> RoleSchema | None:
        try:
            await self.db.update_obj(RoleModel, where_value=[(RoleModel.id, role_id)], update_values=data)
            return await self.get(role_id)
        except IntegrityError:
            logger.error(RoleAlreadyExist('Role already exist'))
            return None

    async def delete(self, role_id: UUID) -> bool:
        try:
            # Удалю связи
            await self.db.delete_obj(
                UserRoleAssociationModel, where_value=[(UserRoleAssociationModel.role_id, role_id)]
            )

            # Удаляю роль
            await self.db.delete_obj(RoleModel, where_value=[(RoleModel.id, role_id)])
            return True
        except Exception as err:
            logger.error('Can not delete role_id=%s error=%s', role_id, err)
            return False
