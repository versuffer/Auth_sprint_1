import uuid

from app.exceptions import RoleNotFoundError, UserNotFoundError
from app.schemas.api.v1.roles_schemas import (
    AssignUserRoleResponseSchema,
    GetUserRolesResponseSchema,
    RevokeUserRoleResponseSchema,
    RoleSchema,
    RolesSchema,
)
from app.services.auth.user_service import UserRepository


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


class UserRoleService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.roles_repository = RolesRepository()

    async def get_user_roles(self, user_id: uuid.UUID) -> GetUserRolesResponseSchema:
        user = await self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundError
        return GetUserRolesResponseSchema(user_id=user_id, roles=user.roles)

    async def assign_user_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> AssignUserRoleResponseSchema:
        user = await self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundError
        role = await self.roles_repository.get(role_id)
        if not role:
            raise RoleNotFoundError
        user = await self.user_repository.add_user_role(user_id, role_id)
        return AssignUserRoleResponseSchema(user_id=user_id, roles=user.roles)

    async def revoke_user_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> RevokeUserRoleResponseSchema:
        user = await self.user_repository.get(user_id)
        if not user:
            raise UserNotFoundError
        role = await self.roles_repository.get(role_id)
        if not role:
            raise RoleNotFoundError
        user = await self.user_repository.delete_user_role(user_id, role_id)
        return RevokeUserRoleResponseSchema(user_id=user_id, roles=user.roles)
