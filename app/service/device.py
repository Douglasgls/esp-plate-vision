from typing import List, Optional
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate

class DeviceService:

    @staticmethod
    async def list_all() -> List[Device]:
        return await Device.all().prefetch_related("spot")

    @staticmethod
    async def get_by_id(device_id: int) -> Optional[Device]:
        return await Device.get_or_none(id=device_id).prefetch_related("spot")

    @staticmethod
    async def create(data: DeviceCreate) -> Device:
        device = await Device.create(**data.dict())
        return device

    @staticmethod
    async def update(device_id: int, data: DeviceUpdate) -> Optional[Device]:
        device = await Device.get_or_none(id=device_id)
        if not device:
            return None
        
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(device, field, value)
        
        await device.save()
        return device

    @staticmethod
    async def delete(device_id: int) -> bool:
        deleted_count = await Device.filter(id=device_id).delete()
        return deleted_count > 0
