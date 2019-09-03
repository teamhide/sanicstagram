from sqlalchemy import (Column, BigInteger, Unicode, ForeignKey, Table)
from sqlalchemy.orm import relationship, backref

from core.databases import Base
from core.databases.mixin import TimestampMixin

post_tag = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)
post_attachment = Table(
    'post_attachment',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('attachment_id', ForeignKey('attachments.id'), primary_key=True),
)
post_comment = Table(
    'post_comment',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('comment_id', ForeignKey('comments.id'), primary_key=True),
)
comment_tag = Table(
    'comment_tag',
    Base.metadata,
    Column('post_id', ForeignKey('comments.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)


class Post(Base, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    attachments = relationship(
        'Attachment',
        secondary=post_attachment,
        lazy='subquery',
        backref=backref('posts', lazy=True)
    )
    caption = Column(Unicode(length=255), nullable=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User')
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
    likes = relationship('PostLike')


class Comment(Base, TimestampMixin):
    __tablename__ = 'comments'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    body = Column(Unicode(length=200), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User')
    tags = relationship(
        'Tag',
        secondary=comment_tag,
        lazy='subquery',
        backref=backref('comments', lazy=True),
    )


class Attachment(Base, TimestampMixin):
    __tablename__ = 'attachments'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    path = Column(Unicode(length=255), nullable=False)


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(Unicode(length=50), nullable=False)


class PostLike(Base, TimestampMixin):
    __tablename__ = 'post_like'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    post_id = Column(ForeignKey('posts.id'), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User')
