import uuid

from app.schemas.api.v1.roles_schemas import RoleSchema, RolesSchema


class RolesRepository:
    async def get_all(self) -> RolesSchema:
        pass

    async def get(self, role_id: uuid.UUID) -> RoleSchema:
        pass

    async def create(self, role_data: RoleSchema) -> RoleSchema:
        pass

    async def delete(self, role_id: uuid.UUID) -> None:
        pass


class RolesService:
    def __init__(self):
        self.roles_repository = RolesRepository()

    async def get_roles(self) -> RolesSchema:
        return await self.roles_repository.get_all()

    async def get_role(self, role_id: uuid.UUID) -> RoleSchema:
        return await self.roles_repository.get(role_id)

    async def create_role(self, role_data: RoleSchema) -> RoleSchema:
        return await self.roles_repository.create(role_data)

    async def delete_role(self, role_id: uuid.UUID) -> None:
        return await self.roles_repository.delete(role_id)
