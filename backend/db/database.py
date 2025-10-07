# db/database.py (最终的、适用于FastAPI的正确版本)

from contextlib import asynccontextmanager
from typing import AsyncIterator # 【新增】导入 AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from config import DATABASE_URL

async_engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False, pool_size=70, pool_recycle=1800, max_overflow=100
)
AsyncSessionLocal: sessionmaker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# 【修改1】将 get_db 重命名为 get_session。它现在是内部使用的会话管理器。
@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    """
    提供一个异步的数据库会话上下文管理器。
    """
    db = AsyncSessionLocal()
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()

# 【修改2】创建一个新的 get_db 函数，专门用作 FastAPI 的依赖项。
async def get_db() -> AsyncIterator[AsyncSession]:
    """
    一个用作 FastAPI 依赖项的异步生成器。
    它会正确地处理会话的生命周期。
    """
    async with get_session() as session:
        yield session


# --- 共享模型基类 ---
metadata = MetaData()
Base = declarative_base(metadata=metadata)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")