from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import app_settings

async_engine = create_async_engine(url=app_settings.POSTGRES_DSN, echo=False)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)
