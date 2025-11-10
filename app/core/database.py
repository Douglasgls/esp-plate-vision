from tortoise import Tortoise

DATABASE_URL = "mysql://root:admin@localhost:3306/DOUGLASTESTE"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.client",
                "app.models.spot",
                "app.models.device",
                "app.models.reservation",
            ],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print("✅ Banco de dados inicializado com sucesso.")
