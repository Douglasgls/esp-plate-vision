from pydantic import BaseModel
from typing import Optional


class SpotBase(BaseModel):
    spot: int
    sector: str


class SpotCreate(SpotBase):
    spot: int
    sector: str


class SpotUpdate(BaseModel):
    spot: Optional[int] = None
    sector: Optional[str] = None

class SpotOut(SpotBase):
    id: int

    class Config:
        orm_mode = True
