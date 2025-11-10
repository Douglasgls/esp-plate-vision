from pydantic import BaseModel
from typing import Optional


class SpotBase(BaseModel):
    name: str


class SpotCreate(SpotBase):
    pass


class SpotUpdate(BaseModel):
    name: Optional[str] = None


class SpotOut(SpotBase):
    id: int

    class Config:
        orm_mode = True
