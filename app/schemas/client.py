from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientBase(BaseModel):
    name: str
    cpf: str
    phone: Optional[str] = None
    email: EmailStr
    vehicle_plate: Optional[str] = None


class ClientCreate(ClientBase):
    pass  


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    vehicle_plate: Optional[str] = None


class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
