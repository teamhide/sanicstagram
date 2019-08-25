from sqlalchemy import Column, ForeignKey, BigInteger
from core.databases import Base
from core.databases.mixin import TimestampMixin


class Follow(Base, TimestampMixin):
    __tablename__ = 'follows'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    follower = Column(
        BigInteger,
        ForeignKey('users.id'),
        nullable=False,
        primary_key=True,)
    following = Column(
        BigInteger,
        ForeignKey('users.id'),
        nullable=False,
        primary_key=True,
    )
