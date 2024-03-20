from sqlalchemy.orm import relationship
from local_databases import postgresql
from sqlalchemy import Column, ForeignKey, String

from db_entities.users import User


class Thread(postgresql.Base):
    __tablename__ = 'threads'

    id = Column(String(50), primary_key=True, nullable=False, unique=True)
    user_id = Column(ForeignKey(User.id), nullable=False)

    user = relationship(User.__name__, lazy='joined')
