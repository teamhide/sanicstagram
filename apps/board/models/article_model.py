from sqlalchemy import (Column, BigInteger, Unicode)

from core.databases import Base
from core.databases.mixin import TimestampMixin


class Article(Base, TimestampMixin):
    __tablename__ = 'boards'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    pw = Column(Unicode(length=30), nullable=False)
    subject = Column(Unicode(length=30), nullable=False)
    content = Column(Unicode(length=500), nullable=False)

    def __repr__(self):
        return '<Article: {}>'.format(self.id)
