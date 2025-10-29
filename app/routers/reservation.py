from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationOut
from app.service.reservation import ReservationService

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ReservationOut])
async def list_reservations():
    return await ReservationService.list_all()

@router.get("/{reservation_id}", response_model=ReservationOut)
async def get_reservation(reservation_id: int):
    reservation = await ReservationService.get_by_id(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.post("/", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
async def create_reservation(data: ReservationCreate):
    return await ReservationService.create(data)

@router.patch("/{reservation_id}", response_model=ReservationOut)
async def update_reservation(reservation_id: int, data: ReservationUpdate):
    reservation = await ReservationService.update(reservation_id, data)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(reservation_id: int):
    success = await ReservationService.delete(reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return None
