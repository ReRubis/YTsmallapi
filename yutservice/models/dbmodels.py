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

    videoId = Column(
        String,
        nullable=False,
        unique=True,
        primary_key=True,
    )


class YouTubeVideos(Base):

    channelTitle = Column(String)
    thumbnail = Column(String)
    title = Column(String)
