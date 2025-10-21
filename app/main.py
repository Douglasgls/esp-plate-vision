from fastapi import FastAPI
from tortoise import Tortoise
from contextlib import asynccontextmanager

from app.models.user import User

from app.routers.plate import router as plate_router
from app.routers.user import router as user_router

from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("======== STARTED-DB & SCHEMA GENERATED ========")

    await init_db()
    
    user_jane = await User.create(name="Jane_Doe", email="jane@email.com", password="5678")
    print("Usuário temporário Jane criado:", user_jane)

    yield 

    try:
        user_to_delete = await User.get(name="Jane_Doe")
        await user_to_delete.delete()
        print(f"Usuário {user_to_delete.name} excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao deletar usuário Jane: {e}")
    await Tortoise.close_connections()
    print("======== FINISH-DB & CONNECTIONS CLOSED ========")

app = FastAPI(
    title="EncontraPlaca API",
    description="API para detecção e validação de placas de veículos no Brasil",
    version="1.0.0",
    contact={
        "name": "Douglas Paz",
        "url": "https://github.com/douglasgls",
    },
    lifespan=lifespan
)

# Routers
app.include_router(
    prefix="/api",
    router=plate_router
)

app.include_router(
    prefix="/api",
    router=user_router
)

@app.get("/")
def read_root():
    return {"Hello": "World"}