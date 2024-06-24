import uuid

from app.exceptions import RoleNotFoundError, UserNotFoundError
from app.schemas.api.v1.roles_schemas import (
    AssignUserRoleResponseSchema,
    RevokeUserRoleResponseSchema,
)
from app.schemas.services.auth.role_service_schemas import RoleSchema, RoleSchemaCreate
from app.services.auth.user_service import UserRepository
from app.services.repositories.role_repository import RoleRepository


class RolesService:
    def __init__(self):
        self.role_repository = RoleRepository()

    async def get_roles(self) -> list[RoleSchema]:
        return [RoleSchema.validate(role) for role in await self.role_repository.get_all()]

    async def get_role(self, role_id: uuid.UUID) -> RoleSchema:
        return await self.role_repository.get(role_id)

    async def create_role(self, role_data: RoleSchemaCreate) -> RoleSchema:
        return await self.role_repository.create(role_data)

    async def delete_role(self, role_id: uuid.UUID) -> bool:
        return await self.role_repository.delete(role_id)


class UserRoleService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()

    async def get_user_roles(self, user_id: uuid.UUID) -> list[RoleSchema]:
        user = await self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundError
        return [RoleSchema.model_validate(role) for role in user.roles]

    async def assign_user_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> AssignUserRoleResponseSchema:
        user = await self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundError
        role = await self.role_repository.get(role_id)
        if not role:
            raise RoleNotFoundError
        user = await self.user_repository.add_user_role(user_id, role_id)
        return AssignUserRoleResponseSchema(user_id=user_id, roles=user.roles)

    async def revoke_user_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> RevokeUserRoleResponseSchema:
        user = await self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundError
        role = await self.role_repository.get(role_id)
        if not role:
            raise RoleNotFoundError
        user = await self.user_repository.delete_user_role(user_id, role_id)
        return RevokeUserRoleResponseSchema(user_id=user_id, roles=user.roles)
