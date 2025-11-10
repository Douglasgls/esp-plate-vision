from fastapi import FastAPI
from tortoise import Tortoise

from contextlib import asynccontextmanager
from app.core.database import init_db

from app.models.user import User

from app.routers.plate import router as plate_router

from app.routers.user import router as user_router

from app.routers.client import router as client_router

from app.routers.spot import router as spot_router

from app.routers.device import router as device_router

from app.routers.reservation import router as reservation_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("======== STARTED-DB & SCHEMA GENERATED ========")

    await init_db()
    
    await User.create(name="Jane_Doe", email="jane@email.com", password="5678")

    yield 

    try:
        user_to_delete = await User.get(name="Jane_Doe")
        await user_to_delete.delete()
    except Exception as e:
        pass
    await Tortoise.close_connections()
    
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

app.include_router(
    prefix="/api",
    router=client_router)

app.include_router(
    prefix="/api",
    router=spot_router)

app.include_router(
    prefix="/api", 
    router=device_router)

app.include_router(
    prefix="/api", 
    router=reservation_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}