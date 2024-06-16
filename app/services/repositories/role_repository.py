from uuid import UUID

from app.db.postgres.models.users import RoleModel
from sqlalchemy import select, update, delete
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.api.v1.roles_schemas import RoleSchema


class RoleRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _check_exists_role(self, role_id: UUID | None = None, title: str | None = None) -> bool:
        if not role_id and not title:
            raise ValueError("Either 'id' or 'title' must be provided.")

        if role_id:
            query = select(RoleModel).where(RoleModel.id == role_id)
        else:
            query = select(RoleModel).where(RoleModel.title == title)

        result = await self.session.execute(query)
        return result.scalars().first() is not None

    async def get_all(self) -> Sequence[RoleSchema]:
        query = select(RoleModel)
        result = await self.session.execute(query)
        return [RoleSchema.model_validate(role_db_obj) for role_db_obj in result.scalars().all()]

    async def get(self, role_id: UUID) -> RoleSchema:
        query = select(RoleModel).where(RoleModel.id == role_id)
        result = await self.session.execute(query)
        return RoleSchema.model_validate(result.scalars().first())

    async def create(self, title: str, description: str) -> RoleSchema | None:

        try:
            role = RoleModel(title=title, description=description)
            self.session.add(role)
            await self.session.commit()
        except Exception as err:
            await self.session.rollback()
            return None
        return RoleSchema.validate(role)

    async def update(self, role_id: UUID, data: dict) -> RoleSchema | None:
        query = update(RoleModel).where(RoleModel.id == role_id).values(**data)
        try:
            await self.session.execute(query)
            await self.session.commit()
            updated_role = await self.session.execute(select(RoleModel).where(RoleModel.id == role_id))
            return RoleSchema.model_validate(updated_role.scalars().one_or_none())
        except Exception as err:
            await self.session.rollback()
            return None

    async def delete(self, role_id: UUID) -> bool:
        try:
            role_exist = await self._check_exists_role(role_id=role_id)
            if role_exist:
                query = delete(RoleModel).where(RoleModel.id == role_id)
                await self.session.execute(query)
                await self.session.commit()
                return True
        except Exception as err:
            await self.session.rollback()
            return False
