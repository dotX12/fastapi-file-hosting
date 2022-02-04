import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings_app


DATABASE_URL = settings_app.dsn
engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)
