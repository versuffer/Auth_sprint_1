from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.docs.tags import ApiTags
from app.api.error_decorators import handle_errors
from app.schemas.api.v1.roles_schemas import RoleResponseSchema
from app.services.auth.auth_service import AuthenticationService
from app.services.auth.role_services import UserRoleService
from app.services.fastapi.dependencies import get_bearer_token

users_router = APIRouter(prefix='/users')


@users_router.get(
    '/{user_id}/roles',
    status_code=status.HTTP_200_OK,
    summary='Получить все роли пользователя',
    response_model=list[RoleResponseSchema],
    tags=[ApiTags.V1_USERS],
)
@handle_errors
async def get_user_roles(
    user_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    user_role_service: UserRoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    return await user_role_service.get_user_roles(user_id)


@users_router.post(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Назначить роль пользователю',
    tags=[ApiTags.V1_USERS],
)
@handle_errors
async def assign_user_role(
    user_id: UUID,
    role_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    user_role_service: UserRoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    await user_role_service.assign_user_role(user_id, role_id)
    return {'detail': 'Successful assign'}


@users_router.delete(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Отозвать роль у пользователя',
    tags=[ApiTags.V1_USERS],
)
@handle_errors
async def revoke_user_role(
    user_id: UUID,
    role_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    user_role_service: UserRoleService = Depends(),
):
    await auth_service.authorize_superuser(access_token=access_token)
    await user_role_service.revoke_user_role(user_id, role_id)
    return {'detail': 'Successful revoke'}
