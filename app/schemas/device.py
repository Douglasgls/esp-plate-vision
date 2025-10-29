from pydantic import BaseModel, constr
from typing import Optional, Literal
from datetime import datetime

class DeviceBase(BaseModel):
    spot_id: int
    status: Literal["active", "inactive", "error"]
    chip_id: constr(max_length=50)
    last_communication: Optional[datetime] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    spot_id: Optional[int] = None
    status: Optional[Literal["active", "inactive", "error"]] = None
    chip_id: Optional[constr(max_length=50)] = None
    last_communication: Optional[datetime] = None


class DeviceOut(DeviceBase):
    id: int

    class Config:
        orm_mode = True
