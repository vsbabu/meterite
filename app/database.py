from . import config

import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database = databases.Database(config.Settings().database_url)

engine = sqlalchemy.create_engine(
    config.Settings().database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get sqlalchemy orm session"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
