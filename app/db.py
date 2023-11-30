import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_async_engine(os.getenv('DATABASE_URL'))
AsyncSessionLocal: type[AsyncSession] = sessionmaker(bind=engine, class_=AsyncSession)
Base = declarative_base()
