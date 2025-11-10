from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.spot import SpotCreate, SpotUpdate, SpotOut
from app.service.spot import SpotService

router = APIRouter(
    prefix="/spots",
    tags=["spots"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[SpotOut])
async def list_spots():
    """Lista todas as vagas cadastradas."""
    return await SpotService.list_all()


@router.get("/{spot_id}", response_model=SpotOut)
async def get_spot(spot_id: int):
    """Busca uma vaga pelo ID."""
    spot = await SpotService.get_by_id(spot_id)
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot


@router.post("/", response_model=SpotOut, status_code=status.HTTP_201_CREATED)
async def create_spot(spot: SpotCreate):
    """Cria uma nova vaga."""
    return await SpotService.create(spot)


@router.patch("/{spot_id}", response_model=SpotOut)
async def update_spot(spot_id: int, data: SpotUpdate):
    """Atualiza os dados de uma vaga existente."""
    spot = await SpotService.update(spot_id, data)
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    return spot


@router.delete("/{spot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_spot(spot_id: int):
    """Deleta uma vaga pelo ID."""
    success = await SpotService.delete(spot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Spot not found")
    return None
