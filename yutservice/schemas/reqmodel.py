from pydantic import BaseModel
from typing import Optional


class SearchReq(BaseModel):
    q: str
    page_token: Optional[str] = None
    publishedAfter: Optional[str] = None
    publishedBefore: Optional[str] = None


class VideoId(BaseModel):
    video_id: str


class RequestLogIn(BaseModel):
    email: str
    password: str


class RequestRegistration(BaseModel):
    email: str
    password: str
