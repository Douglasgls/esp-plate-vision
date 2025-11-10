from pydantic import BaseModel, Field, constr
from typing import Optional, Literal
from datetime import datetime


class DeviceBase(BaseModel):
    spot_id: int = Field(..., description="ID da vaga associada ao dispositivo")
    status: Literal["ATIVO", "INATIVO", "ERRO"] = Field(..., description="Status atual do dispositivo")
    chip_id: constr(max_length=50) = Field(..., description="Identificador único do chip do dispositivo")


class DeviceCreate(DeviceBase):
    """Schema usado para criar um novo dispositivo."""
    pass


class DeviceUpdate(BaseModel):
    """Schema usado para atualização parcial (PATCH) do dispositivo."""
    spot_id: Optional[int] = Field(None, description="Novo ID da vaga associada")
    status: Optional[Literal["active", "inactive", "error"]] = Field(None, description="Novo status do dispositivo")
    chip_id: Optional[constr(max_length=50)] = Field(None, description="Novo identificador de chip")
    last_communication: Optional[datetime] = Field(None, description="Data/hora atualizada da última comunicação")


class DeviceOut(DeviceBase):
    """Schema de saída com o ID do dispositivo."""
    id: int

    class Config:
        orm_mode = True
