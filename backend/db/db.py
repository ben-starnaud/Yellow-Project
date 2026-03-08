from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# The Engine is the only part of your code that actually knows how to talk to Postgres. It manages a "Pool" of connections so you don't have to open and close a new one every single time.
engine = create_async_engine(DATABASE_URL, echo=True) # prints the Raw SQL that SQLAlchemy generates to your terminal.

# Every time a user hits your API, a new session is born. This session handles that one user’s request, tracks their changes, and then dies when the request is over.
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) 

# This Base class is what your models will inherit from. It maintains a catalog of classes and tables relative to that base.
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

