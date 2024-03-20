from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import inspect
from typing import Callable

from OpenAIChatAPI.constants import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=100,
    max_overflow=0,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData(bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def connected_to_db(function: Callable):
    if inspect.isawaitable(function):
        async def connect(*args, **kwargs):
            ses = None
            try:
                ses: Session = SessionLocal()
                data = await function(*args, **kwargs, session=ses)
            finally:
                if ses:
                    ses.close()

            return data

        return connect
    else:
        def connect(*args, **kwargs):
            ses = None
            try:
                ses = SessionLocal()
                data = function(*args, **kwargs, session=ses)
            finally:
                if ses:
                    ses.close()

            return data

        return connect
