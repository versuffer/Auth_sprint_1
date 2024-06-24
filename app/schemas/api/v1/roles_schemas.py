import uuid

from pydantic import BaseModel

from app.schemas.services.auth.role_service_schemas import RoleSchema


class GetRolesResponseSchema(RoleSchema):
    pass


class GetRoleResponseSchema(RoleSchema):
    pass


class CreateRoleResponseSchema(RoleSchema):
    pass


class GetUserRolesResponseSchema(BaseModel):
    user_id: uuid.UUID
    roles: list[RoleSchema]


class AssignUserRoleResponseSchema(GetUserRolesResponseSchema):
    pass


class RevokeUserRoleResponseSchema(GetUserRolesResponseSchema):
    pass
