from sqlalchemy import (Column, BigInteger, Unicode, Table, ForeignKey,
                        UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from core.databases import Base
from core.databases.mixin import TimestampMixin

follows = Table(
    'follows',
    Base.metadata,
    Column('follower_id', BigInteger, ForeignKey('users.id')),
    Column('following_id', BigInteger, ForeignKey('users.id')),
    UniqueConstraint('follower_id', 'following_id', name='unique_follows')
)


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    GENDER_TYPES = [
        (u'm', u'M'),
        (u'f', u'F'),
        (u'u', u'Unknown'),
    ]

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(Unicode(length=255), nullable=True)
    website = Column(Unicode(length=50), nullable=True)
    bio = Column(Unicode(length=50), nullable=True)
    phone = Column(Unicode(length=20), nullable=True)
    gender = Column(ChoiceType(GENDER_TYPES))
    follower = relationship(
        'User',
        secondary=follows,
        primaryjoin=id==follows.c.follower_id,
    )
    following = relationship(
        'User',
        secondary=follows,
        primaryjoin=id==follows.c.following_id,
    )
