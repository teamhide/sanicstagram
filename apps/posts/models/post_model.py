from sqlalchemy import (Column, BigInteger, Unicode, ForeignKey, Table)
from sqlalchemy.orm import relationship, backref

from core.databases import Base
from core.databases.mixin import TimestampMixin


post_tag = Table(
    'post_tag',
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)
comment_tag = Table(
    'comment_tag',
    Column('post_id', ForeignKey('comments.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)


class Post(Base, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    images = Column(Unicode(length=255), nullable=False)
    caption = Column(Unicode(length=255), nullable=True)
    creator = Column(ForeignKey('users.id'), nullable=False)
    tags = relationship(
        'Tag',
        secondary=post_tag,
        lazy='subquery',
        backref=backref('posts', lazy=True),
    )


class Comment(Base, TimestampMixin):
    __tablename__ = 'comments'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    message = Column(Unicode(length=200), nullable=False)
    creator = Column(ForeignKey('users.id'), nullable=False)
    tags = relationship(
        'Tag',
        secondary=comment_tag,
        lazy='subquery',
        backref=backref('comments', lazy=True),
    )


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(Unicode(length=50), nullable=False)
