from tkinter.messagebox import NO
from pydantic import BaseModel


class Item(BaseModel):
    videoId: str | None
    thumbnail: str | None
    title: str | None
    channelTitle: str | None
    publishedAt: str | None

    class Config:
        from_attributes = True


class YouTubeSearchResponce(BaseModel):
    nextPageToken: str | None
    prevPageToken: str | None
    items: list[Item] = []

    class Config:
        from_attributes = True
