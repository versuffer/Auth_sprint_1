import uuid

from app.exceptions import RoleAlreadyExistsError, RoleNotFoundError, UserNotFoundError
from app.schemas.api.v1.roles_schemas import (
    AssignUserRoleResponseSchema,
    RevokeUserRoleResponseSchema,
)
from app.schemas.services.auth.role_service_schemas import RoleSchema, RoleSchemaCreate
from app.services.repositories.role_repository import role_repository
from app.services.repositories.user_repository import user_repository


class RoleService:
    def __init__(self):
        self.role_repository = role_repository

    async def get_roles(self) -> list[RoleSchema]:
        return [RoleSchema.validate(role) for role in await self.role_repository.get_all()]

    async def get_role(self, role_id: uuid.UUID) -> RoleSchema:
        if not (role := await self.role_repository.get(role_id)):
            raise RoleNotFoundError

        return role

    async def create_role(self, role_data: RoleSchemaCreate) -> RoleSchema:
        if await self.role_repository.get_by_title(role_title=role_data.title):
            raise RoleAlreadyExistsError

        return await self.role_repository.create(role_data)

    async def delete_role(self, role_id: uuid.UUID) -> bool:
        if not await self.role_repository.get(role_id):
            raise RoleNotFoundError

        return await self.role_repository.delete(role_id)


class UserRoleService:
    def __init__(self):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def get_user_roles(self, user_id: uuid.UUID) -> list[RoleSchema]:
        if not (user := await self.user_repository.get(user_id)):
            raise UserNotFoundError
        return [RoleSchema.model_validate(role) for role in user.roles]

    async def assign_user_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> AssignUserRoleResponseSchema:
        if not await self.user_repository.get(user_id):
            raise UserNotFoundError
        if not await self.role_repository.get(role_id):
            raise RoleNotFoundError

        user = await self.user_repository.add_user_role(user_id, role_id)
        return AssignUserRoleResponseSchema(user_id=user_id, roles=user.roles)

    async def revoke_user_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> RevokeUserRoleResponseSchema:
        if not await self.user_repository.get(user_id):
            raise UserNotFoundError
        if not await self.role_repository.get(role_id):
            raise RoleNotFoundError

        user = await self.user_repository.delete_user_role(user_id, role_id)
        return RevokeUserRoleResponseSchema(user_id=user_id, roles=user.roles)
