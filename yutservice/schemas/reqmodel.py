from pydantic import BaseModel


class SearchReq(BaseModel):
    q: str
    page_token: str | None
    publishedAfter: str | None
    publishedBefore: str | None


class VideoId(BaseModel):
    video_id: str


class RequestLogIn(BaseModel):
    email: str
    password: str


class RequestRegistration(BaseModel):
    email: str
    password: str
