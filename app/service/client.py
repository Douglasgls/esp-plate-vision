from typing import List, Optional
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    """Service layer para operações CRUD de clientes."""

    @staticmethod
    async def list_all() -> List[Client]:
        """Retorna todos os clientes cadastrados."""
        return await Client.all()

    @staticmethod
    async def get_by_id(cliente_id: int) -> Optional[Client]:
        """Busca um cliente pelo ID."""
        return await Client.get_or_none(id=cliente_id)

    @staticmethod
    async def create(data: ClientCreate) -> Client:
        """Cria um novo cliente."""
        cliente = await Client.create(**data.dict())
        return cliente

    @staticmethod
    async def update(cliente_id: int, data: ClientUpdate) -> Optional[Client]:
        """Atualiza os dados de um cliente existente."""
        cliente = await Client.get_or_none(id=cliente_id)
        if not cliente:
            return None

        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cliente, field, value)

        await cliente.save()
        return cliente

    @staticmethod
    async def delete(cliente_id: int) -> bool:
        """Deleta um cliente pelo ID."""
        deleted_count = await Client.filter(id=cliente_id).delete()
        return deleted_count > 0
