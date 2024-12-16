import asyncio
from config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = Config.RENDER_DATA_BASE_URL

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,         
    max_overflow=10,        
    pool_timeout=10,
    pool_recycle=1800,
    pool_pre_ping=True        
)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
