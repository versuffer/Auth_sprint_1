from uuid import UUID

from fastapi import APIRouter, status

from app.api.docs.tags import ApiTags

roles_router = APIRouter(prefix='/roles')


@roles_router.get(
    '',
    status_code=status.HTTP_200_OK,
    summary='Получить все существующие роли',
    # response_model=GetRolesResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def get_roles(
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    pass


@roles_router.get(
    '/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Получить роль по id',
    # response_model=GetRoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def get_role(
    role_id: UUID,
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    pass


@roles_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    summary='Создать роль',
    # response_model=CreateRoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def create_role(
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    pass


@roles_router.delete(
    '/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить роль',
    # response_model=DeleteRoleResponseSchema,
    tags=[ApiTags.V1_ROLES],
)
async def delete_role(
    role_id: UUID,
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    pass
