from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceOut
from app.service.device import DeviceService

router = APIRouter(
    prefix="/device",
    tags=["device"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[DeviceOut])
async def list_devices():
    return await DeviceService.list_all()

@router.get("/{device_id}", response_model=DeviceOut)
async def get_device(device_id: int):
    device = await DeviceService.get_by_id(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceCreate):
    return await DeviceService.create(device)

@router.patch("/{device_id}", response_model=DeviceOut)
async def update_device(device_id: int, data: DeviceUpdate):
    device = await DeviceService.update(device_id, data)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: int):
    success = await DeviceService.delete(device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return None
