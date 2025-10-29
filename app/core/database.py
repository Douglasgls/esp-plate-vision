from tortoise import Tortoise
from app.models.user import User


DATABASE_URL = "mysql://root:admin@localhost:3306/DOUGLASTESTE"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models",],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()