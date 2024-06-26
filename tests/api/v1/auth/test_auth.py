import pytest
from httpx import AsyncClient

from app.main import app
from app.schemas.api.v1.auth_schemas import (
    RegisterResponseSchema,
    RegisterUserCredentialsSchema,
)
from app.services.repositories.user_repository import user_repository


@pytest.mark.anyio
class TestAuthentication:
    async def test_register_201(self, async_test_client: AsyncClient):
        # Arrange
        user_data = RegisterUserCredentialsSchema(
            username='random_username', email='random@email.com', password='random_password'
        )
        user_data_json = user_data.model_dump(mode='json')

        # Act
        response = await async_test_client.post(app.url_path_for('api_v1_register'), json=user_data_json)
        response_json = response.json()

        # Assert
        assert response_json == RegisterResponseSchema(**response_json).model_dump(mode='json')
        assert await user_repository.get(user_id=response_json['id'])
