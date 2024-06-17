import uuid

from pydantic import BaseModel, ConfigDict


class RoleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str


class RolesSchema(BaseModel):
    roles: list[RoleSchema]


class GetRolesResponseSchema(RolesSchema):
    pass


class GetRoleResponseSchema(RoleSchema):
    pass


class CreateRoleResponseSchema(RoleSchema):
    pass


class GetUserRolesResponseSchema(BaseModel):
    user_id: uuid.UUID
    roles: RolesSchema


class AssignUserRoleResponseSchema(GetUserRolesResponseSchema):
    pass


class RevokeUserRoleResponseSchema(GetUserRolesResponseSchema):
    pass
