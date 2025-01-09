from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database url for authorization service
DATABASE_URL = "sqlite:///./auth.db"

"""
    Create connection to db (SQLite).
    connect_args - parameter to disable thread check.
"""
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

"""
    Crete factory for generating 'Session' objects

    SessionLocal - object for working with database.
    autocommit - Indicates that transactions will not be committed automatically. 
        You need to manually call session.commit() to save changes.
    autoflush - Turns off the automatic updating of data in the database before executing queries. 
        This gives you more control over when the data should be written.
    bind - Associates a session with a specific engine object so that it knows which database to access.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creates a base class for all models (tables) in the database.
Base = declarative_base()

"""
    MetaData

    An object that stores a database schema 
    (all tables, their columns, relationships, etc.). 
    It is used to create and manage a database.
"""
metadata = MetaData()
