from tkinter.messagebox import NO
from pydantic import BaseModel


class Item(BaseModel):
    videoId: str
    thumbnail: str
    title: str
    channelTitle: str
    publishedAt: str | None

    class Config:
        orm_mode = True


class YouTubeSearchResponce(BaseModel):
    nextPageToken: str | None
    prevPageToken: str | None
    items: list[Item] = []

    class Config:
        orm_mode = True
