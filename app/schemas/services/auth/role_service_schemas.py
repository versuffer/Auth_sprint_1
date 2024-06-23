import uuid

from pydantic import BaseModel, ConfigDict


class RoleSchemaCreate(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class RoleSchema(RoleSchemaCreate):
    id: uuid.UUID
    title: str
    description: str
