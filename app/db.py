from settings import database_url, DEBUG
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


sqlalchemy_engine = create_async_engine(database_url, echo=DEBUG)
session = sessionmaker(bind=sqlalchemy_engine)

async_session = sessionmaker(
        sqlalchemy_engine, expire_on_commit=False, class_=AsyncSession
)


