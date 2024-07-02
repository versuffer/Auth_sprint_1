from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.docs.tags import ApiTags
from app.api.error_decorators import handle_errors
from app.schemas.api.v1.roles_schemas import RoleResponseSchema
from app.schemas.services.auth.role_service_schemas import (
    CreateRoleSchema,
    PartialUpdateRoleSchema,
)
from app.services.auth.auth_service import AuthenticationService
from app.services.auth.role_services import RoleService
from app.services.fastapi.dependencies import get_bearer_token

roles_router = APIRouter(prefix='/roles')


@roles_router.get(
    '',
    status_code=status.HTTP_200_OK,
    summary='Получить все существующие роли',
    response_model=list[RoleResponseSchema],
    tags=[ApiTags.V1_ROLES],
)
@handle_errors
async def get_roles(
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    return await role_service.get_roles()


@roles_router.get(
    '/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Получить роль по id',
    response_model=RoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
@handle_errors
async def get_role(
    role_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    return await role_service.get_role(role_id)


@roles_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    summary='Создать роль',
    response_model=RoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
@handle_errors
async def create_role(
    role_data: CreateRoleSchema,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    return await role_service.create_role(role_data)


@roles_router.patch(
    '/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Изменить роль',
    response_model=RoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
@handle_errors
async def partially_update_role(
    role_id: UUID,
    role_data: PartialUpdateRoleSchema,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    return await role_service.partially_update_role(role_id=role_id, role_data=role_data)


@roles_router.delete(
    '/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить роль',
    tags=[ApiTags.V1_ROLES],
)
@handle_errors
async def delete_role(
    role_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    await role_service.delete_role(role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
