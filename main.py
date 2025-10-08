from fastapi import FastAPI
from routers import plate


app = FastAPI(
    title="EncontraPlaca API",
    description="API para detecção e validação de placas de veículos no Brasil",
    version="1.0.0",
    contact={
        "name": "Douglas Paz",
        "url": "https://github.com/douglasgls",
    },
)
app.include_router(
    prefix="/api",
    router=plate.router
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
