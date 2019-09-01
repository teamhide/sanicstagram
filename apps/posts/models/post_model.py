from sqlalchemy import (Column, BigInteger, Unicode, ForeignKey, Table)
from sqlalchemy.orm import relationship, backref

from core.databases import Base
from core.databases.mixin import TimestampMixin

post_tag = Table(
    'post_tag',
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)
post_image = Table(
    'post_image',
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('image_id', ForeignKey('images.id'), primary_key=True),
)
post_comment = Table(
    'post_comment',
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('comment_id', ForeignKey('comments.id'), primary_key=True),
)
comment_tag = Table(
    'comment_tag',
    Column('post_id', ForeignKey('comments.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)


class Post(Base, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    images = relationship(
        'Image',
        secondary=post_image,
        lazy='subquery',
        backref=backref('posts', lazy=True)
    )
    caption = Column(Unicode(length=255), nullable=True)
    creator = Column(ForeignKey('users.id'), nullable=False)
    comments = relationship(
        'Comment',
        secondary=post_comment,
        lazy='subquery',
        backref=backref('posts', lazy=True)

    )
    tags = relationship(
        'Tag',
        secondary=post_tag,
        lazy='subquery',
        backref=backref('posts', lazy=True),
    )


class Comment(Base, TimestampMixin):
    __tablename__ = 'comments'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    body = Column(Unicode(length=200), nullable=False)
    creator = Column(ForeignKey('users.id'), nullable=False)
    tags = relationship(
        'Tag',
        secondary=comment_tag,
        lazy='subquery',
        backref=backref('comments', lazy=True),
    )


class Image(Base, TimestampMixin):
    __tablename__ = 'images'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    path = Column(Unicode(length=255), nullable=False)


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(Unicode(length=50), nullable=False)
