from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.docs.tags import ApiTags
from app.schemas.api.v1.roles_schemas import (
    CreateRoleResponseSchema,
    GetRoleResponseSchema,
    GetRolesResponseSchema,
    RoleSchema,
)
from app.services.auth.role_service import RolesService

roles_router = APIRouter(prefix='/roles')


@roles_router.get(
    '',
    status_code=status.HTTP_200_OK,
    summary='Получить все существующие роли',
    response_model=GetRolesResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def get_roles(
    # access_token: AuthorizationHeader (только для суперпользователей)
    service: RolesService = Depends(),
):
    return await service.get_roles()


@roles_router.get(
    '/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Получить роль по id',
    response_model=GetRoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def get_role(
    role_id: UUID,
    service: RolesService = Depends(),
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    return await service.get_role(role_id)


@roles_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    summary='Создать роль',
    response_model=CreateRoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def create_role(
    # access_token: AuthorizationHeader (только для суперпользователей)
    role_data: RoleSchema,
    service: RolesService = Depends(),
):
    return await service.create_role(role_data)


@roles_router.delete(
    '/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить роль',
    tags=[ApiTags.V1_ROLES],
)
async def delete_role(
    role_id: UUID,
    service: RolesService = Depends(),
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    return await service.delete_role(role_id)
