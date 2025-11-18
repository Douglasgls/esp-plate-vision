from enum import Enum
from tortoise import fields
from tortoise.models import Model 

class SpotState(str, Enum):
    RESERVED = "RESERVADO"
    EMPTY = "LIVRE"

class SpotCurrentState(str, Enum):
    OCCUPIED = "OCUPADO"
    EMPTY = "LIVRE"

class SpotAlertState(str, Enum):
    OCCUPIED = "OCUPADO"

class Spot(Model):
    id = fields.IntField(pk=True)
    number = fields.IntField()
    sector = fields.CharField(max_length=50, null=True)
    status = fields.CharEnumField(
        enum_type=SpotState,
        description="Spot status",
        null=True
    )
    current_status = fields.CharEnumField(
        enum_type=SpotCurrentState,
        description="Spot current status",
        null=True
    )
    alert_status = fields.CharEnumField(
        enum_type=SpotCurrentState,
        description="Spot alert status",
        null=True
    )

    class Meta:
        table = "vagas"
        ordering = ["id"]

    def __str__(self):
        return f"Vaga {self.number} - {self.status.value}"