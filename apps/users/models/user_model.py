from sqlalchemy import (Column, BigInteger, Unicode)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from core.databases import Base
from core.databases.mixin import TimestampMixin


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
    followers = relationship(
        'Follow',
        backref='followers',
        lazy='dynamic',
        foreign_keys='Follow.following_id',
    )
    followings = relationship(
        'Follow',
        backref='followings',
        lazy='dynamic',
        foreign_keys='Follow.follower_id',
    )
