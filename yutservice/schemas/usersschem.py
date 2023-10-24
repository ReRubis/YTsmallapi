from pydantic import EmailStr, BaseModel, UUID4
from typing import Optional


class UserOut(BaseModel):

    email: str

    class Config:
        from_attributes = True
