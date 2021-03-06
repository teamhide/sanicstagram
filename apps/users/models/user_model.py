from sqlalchemy import (Column, BigInteger, Unicode, ForeignKey, Table)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from core.databases import Base
from core.databases.mixin import TimestampMixin

follows = Table(
    'follows',
    Base.metadata,
    Column('follower_id', ForeignKey('users.id')),
    Column('following_id', ForeignKey('users.id')),
)


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    email = Column(Unicode(length=255), nullable=False, unique=True)
    nickname = Column(Unicode(length=255), nullable=True, unique=True)
    profile_image = Column(Unicode(length=255), nullable=True)
    website = Column(Unicode(length=50), nullable=True)
    bio = Column(Unicode(length=50), nullable=True)
    phone = Column(Unicode(length=20), nullable=True)
    gender = Column(Unicode(length=3), nullable=True)
    followers = relationship(
        'User',
        secondary=follows,
        primaryjoin=(follows.c.following_id == id),
        secondaryjoin=(follows.c.follower_id == id),
        lazy='dynamic',
    )
    followings = relationship(
        'User',
        secondary=follows,
        primaryjoin=(follows.c.follower_id == id),
        secondaryjoin=(follows.c.following_id == id),
        lazy='dynamic',
    )

    @hybrid_property
    def follower_count(self) -> int:
        return self.followers.count()

    @hybrid_property
    def following_count(self) -> int:
        return self.followings.count()
