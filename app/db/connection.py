from contextlib import asynccontextmanager
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool


engine = create_async_engine("mysql+aiomysql://root:rootpassword@mysql_master/mydb", poolclass=NullPool)
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

@asynccontextmanager
async def get_session():
    session = async_session_factory()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
