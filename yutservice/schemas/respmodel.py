from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    videoId: Optional[str] = None
    thumbnail: Optional[str] = None
    title: Optional[str] = None
    channelTitle: Optional[str] = None
    publishedAt: Optional[str] = None

    class Config:
        from_attributes = True


class YouTubeSearchResponce(BaseModel):
    items: list[Item] = []

    class Config:
        from_attributes = True
