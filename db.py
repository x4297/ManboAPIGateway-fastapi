from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import CommonConfig


engine = create_async_engine(CommonConfig.db_url, echo=True if CommonConfig.debug else False)
session_maker = async_sessionmaker(engine, expire_on_commit=False)
