import uuid

from pydantic import BaseModel, ConfigDict


class RoleSchema(BaseModel):
    id: uuid.UUID
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)
