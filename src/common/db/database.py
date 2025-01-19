from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def create_engine_and_session(database_url: str):
    """
    Create async engine and session for connection to database.
    """
    engine = create_async_engine(database_url, echo=True)

    """
        Crete factory for generating 'AsyncSession' objects

        async_session - object for working with database.
        autocommit - Indicates that transactions will not be committed automatically. 
            You need to manually call session.commit() to save changes.
        autoflush - Turns off the automatic updating of data in the database before executing queries. 
            This gives you more control over when the data should be written.
        bind - Associates a session with a specific engine object so that it knows which database to access.
    """
    async_session = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False )

    return engine, async_session


async def get_db(async_session: sessionmaker) -> AsyncSession:
    """
    Guarantee async session for work with database.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
