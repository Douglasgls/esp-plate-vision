from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class ReservationBase(BaseModel):
    customer_id: int = Field(..., description="ID do cliente associado à reserva")
    parking_spot_id: int = Field(..., description="ID da vaga de estacionamento")
    vehicle_id: int = Field(..., description="ID do veículo reservado")
    start_time: datetime = Field(..., description="Data e hora de início da reserva")
    end_time: datetime = Field(..., description="Data e hora de término da reserva")
    status: Literal["pending", "active", "completed", "cancelled"] = Field(..., description="Status atual da reserva")


class ReservationCreate(ReservationBase):
    """Schema usado para criar uma nova reserva."""
    pass


class ReservationUpdate(BaseModel):
    """Schema usado para atualização parcial (PATCH) de uma reserva."""
    customer_id: Optional[int] = Field(None, description="Novo ID do cliente")
    parking_spot_id: Optional[int] = Field(None, description="Novo ID da vaga")
    vehicle_id: Optional[int] = Field(None, description="Novo ID do veículo")
    start_time: Optional[datetime] = Field(None, description="Nova data/hora de início")
    end_time: Optional[datetime] = Field(None, description="Nova data/hora de término")
    status: Optional[Literal["pending", "active", "completed", "cancelled"]] = Field(None, description="Novo status da reserva")


class ReservationOut(ReservationBase):
    """Schema de saída com ID e data de registro da reserva."""
    id: int
    reservation_date: datetime = Field(..., description="Data e hora de criação da reserva")

    class Config:
        orm_mode = True
