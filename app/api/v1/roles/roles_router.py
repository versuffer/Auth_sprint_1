from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.docs.tags import ApiTags
from app.exceptions import (
    AuthorizationError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
    TokenError,
    UserNotFoundError,
    auth_error,
    not_found_error,
    role_already_exists_error,
)
from app.schemas.api.v1.roles_schemas import RoleResponseSchema
from app.schemas.services.auth.role_service_schemas import RoleSchemaCreate
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
async def get_roles(
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    try:
        await auth_service.authorize_superuser(access_token=access_token)
    except (TokenError, UserNotFoundError, AuthorizationError):
        raise auth_error

    try:
        return await role_service.get_roles()
    except (TokenError, UserNotFoundError, AuthorizationError):
        raise auth_error


@roles_router.get(
    '/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Получить роль по id',
    response_model=RoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def get_role(
    role_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    try:
        await auth_service.authorize_superuser(access_token=access_token)
    except (TokenError, UserNotFoundError, AuthorizationError):
        raise auth_error

    try:
        return await role_service.get_role(role_id)
    except RoleNotFoundError:
        raise not_found_error


@roles_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    summary='Создать роль',
    response_model=RoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def create_role(
    role_data: RoleSchemaCreate,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    try:
        await auth_service.authorize_superuser(access_token=access_token)
    except (TokenError, UserNotFoundError, AuthorizationError):
        raise auth_error

    try:
        return await role_service.create_role(role_data)
    except RoleAlreadyExistsError:
        raise role_already_exists_error


@roles_router.delete(
    '/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить роль',
    tags=[ApiTags.V1_ROLES],
)
async def delete_role(
    role_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    role_service: RoleService = Depends(),
):
    try:
        await auth_service.authorize_superuser(access_token=access_token)
    except (TokenError, UserNotFoundError, AuthorizationError):
        raise auth_error

    try:
        await role_service.delete_role(role_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except RoleNotFoundError:
        raise not_found_error
