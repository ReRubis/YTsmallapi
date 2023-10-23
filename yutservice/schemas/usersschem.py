from pydantic import EmailStr, BaseModel, UUID4
from typing import Optional


class UserOut(BaseModel):
    id: int
    name: Optional[str] = None
    picture: Optional[str] = None
    email: str
    team_size: Optional[str] = None
    usage: Optional[str] = None
    facebook_id: Optional[str] = None

    class Config:
        from_attributes = True
