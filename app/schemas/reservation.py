from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class ReservationBase(BaseModel):
    client_id: int = Field(..., description="ID do cliente associado à reserva")
    spot_id: int = Field(..., description="ID da vaga de estacionamento")
    start_time: datetime = Field(..., description="Data e hora de início da reserva")
    end_time: datetime = Field(..., description="Data e hora de término da reserva")
    status: Literal["ATIVO", "CONCLUIDO", "CANCELADO"] = Field(..., description="Status atual da reserva")
    status_spot: Literal["ESPERANDO", "EM_USO", "VAZIO"] = Field(..., description="Status atual da vaga de estacionamento")


class ReservationCreate(ReservationBase):
    """Schema usado para criar uma nova reserva."""
    pass


class ReservationUpdate(BaseModel):
    """Schema usado para atualização parcial (PATCH) de uma reserva."""
    client_id: Optional[int] = Field(None, description="Novo ID do cliente")
    spot_id: Optional[int] = Field(None, description="Novo ID da vaga")
    start_time: Optional[datetime] = Field(None, description="Nova data/hora de início")
    end_time: Optional[datetime] = Field(None, description="Nova data/hora de término")
    status: Optional[Literal["ATIVO", "CONCLUIDO", "CANCELADO"]] = Field(None, description="Status atual da reserva")
    status_spot: Optional[Literal["ESPERANDO", "EM_USO", "VAZIO"]] = Field(None, description="Status atual da vaga de estacionamento")


class ReservationOut(ReservationBase):
    """Schema de saída com ID e data de registro da reserva."""
    id: int

    class Config:
        orm_mode = True
