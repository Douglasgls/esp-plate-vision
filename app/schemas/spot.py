from pydantic import BaseModel
from typing import Optional


class SpotBase(BaseModel):
    number: int
    sector: str


class SpotCreate(SpotBase):
    number: int
    sector: str


class SpotUpdate(BaseModel):
    number: Optional[int] = None
    sector: Optional[str] = None
    status : Optional[str] = None
    alert_status : Optional[str] = None

class SpotOut(SpotBase):
    id: int
    current_status: Optional[str] = None
    status: Optional[str] = None
    alert_status: Optional[str] = None

    class Config:
        orm_mode = True
