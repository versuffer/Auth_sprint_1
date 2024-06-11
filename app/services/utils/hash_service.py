from app.schemas.services.utils.hash_service_schemas import HashedRegistrationData


class HashService:
    async def get_hashed_registration_data(self, password: str) -> HashedRegistrationData:
        pass
