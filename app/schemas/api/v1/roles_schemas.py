from pydantic import BaseModel


class RoleSchema(BaseModel):
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
