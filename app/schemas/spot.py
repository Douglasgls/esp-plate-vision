from pydantic import BaseModel
from typing import Optional


class SpotBase(BaseModel):
    number: str
    status: Optional[str] = "available"


class SpotCreate(SpotBase):
    pass


class SpotUpdate(BaseModel):
    number: Optional[str] = None
    status: Optional[str] = None


class SpotOut(SpotBase):
    id: int

    class Config:
        orm_mode = True
