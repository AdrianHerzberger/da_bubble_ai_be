from config import Config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = Config.SQLALCHEMY_DATABASE_URL

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,         
    max_overflow=20,        
    pool_timeout=30,
    pool_pre_ping=True        
)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)