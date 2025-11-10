from typing import List, Optional
from app.models.spot import Spot
from app.schemas.spot import SpotCreate, SpotUpdate


class SpotService:
    """Service layer para operações CRUD de vagas."""

    @staticmethod
    async def list_all() -> List[Spot]:
        """Retorna todas as vagas cadastradas."""
        return await Spot.all()

    @staticmethod
    async def get_by_id(spot_id: int) -> Optional[Spot]:
        """Busca uma vaga pelo ID."""
        return await Spot.get_or_none(id=spot_id)

    @staticmethod
    async def create(data: SpotCreate) -> Spot:
        """Cria uma nova vaga."""
        spot = await Spot.create(**data.dict())
        return spot

    @staticmethod
    async def update(spot_id: int, data: SpotUpdate) -> Optional[Spot]:
        """Atualiza os dados de uma vaga existente."""
        spot = await Spot.get_or_none(id=spot_id)
        if not spot:
            return None

        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(spot, field, value)

        await spot.save()
        return spot

    @staticmethod
    async def delete(spot_id: int) -> bool:
        """Deleta uma vaga pelo ID."""
        deleted_count = await Spot.filter(id=spot_id).delete()
        return deleted_count > 0
