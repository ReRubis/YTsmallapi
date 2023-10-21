import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Identity
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import (as_declarative, declarative_base,
                                        declared_attr)
from sqlalchemy.sql import func


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)


class YouTubeVideo(Base):
    videoId = Column(
        String,
        nullable=False,
        unique=True,
    )
    channelTitle = Column(String)
    thumbnail = Column(String)
    title = Column(String)
    publishedAt = Column(String, nullable=True)


class Channel(Base):

    channelTitle = Column(String)
    channelid = Column(String, unique=True)
    description = Column(String)
    followercount = Column(String)
