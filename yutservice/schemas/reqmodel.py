from pydantic import BaseModel


class SearchReq(BaseModel):
    q: str
    page_token: str | None
