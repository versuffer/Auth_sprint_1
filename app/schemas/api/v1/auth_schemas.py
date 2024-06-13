import datetime
import uuid

from pydantic import BaseModel


class UserCredentialsSchema(BaseModel):
    login: str
    password: str


class UserNewSchema(BaseModel):
    login: str
    hashed_password: str


class BaseLoginDataSchema(BaseModel):
    user_agent: str  # TODO правильно доставать юзер агент


class CredentialsLoginDataSchema(BaseLoginDataSchema, UserCredentialsSchema):
    pass


class RefreshLoginDataSchema(BaseLoginDataSchema):
    refresh_token: str


class UserTokenDataSchema(BaseModel):
    login: str
    roles: list[str]


class UserTokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class RegisterResponseSchema(BaseModel):
    id: uuid.UUID
    login: str
    is_superuser: bool


class HistorySchema(BaseModel):
    id: uuid.UUID
    auth_date: datetime.datetime
    user_agent: str
