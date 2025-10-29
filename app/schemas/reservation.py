from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class ReservationBase(BaseModel):
    user_id: int
    spot_id: int
    vehicle_id: int
    start_time: datetime
    end_time: datetime
    status: Literal["pending", "active", "completed", "cancelled"]


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    user_id: Optional[int] = None
    spot_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[Literal["pending", "active", "completed", "cancelled"]] = None


class ReservationOut(ReservationBase):
    id: int
    reservation_date: datetime

    class Config:
        orm_mode = True
