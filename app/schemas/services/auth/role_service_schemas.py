import uuid

from pydantic import BaseModel, ConfigDict


class RoleSchemaBase(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleSchemaCreate(RoleSchemaBase):
    pass


class RoleSchema(RoleSchemaBase):
    id: uuid.UUID
