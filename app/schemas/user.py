from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    name: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    active: Optional[bool] = None


class UsuarioOut(UsuarioBase):
    id: int
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
