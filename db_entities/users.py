from local_databases import postgresql
from sqlalchemy import Column, String, CHAR, Integer


class User(postgresql.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(CHAR(64), nullable=False)
