from sqlalchemy import (Column, BigInteger, ForeignKey)

from core.databases import Base
from core.databases.mixin import TimestampMixin


class Follow(Base, TimestampMixin):
    __tablename__ = 'follows'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    follower_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    following_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
