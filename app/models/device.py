from tortoise import fields
from tortoise.models import Model
from enum import Enum

class DeviceStatus(str, Enum):
    ACTIVE = "ATIVO"
    INACTIVE = "INATIVO"
    ERROR = "ERRO"

class Device(Model):
    id = fields.IntField(pk=True)
    spot = fields.ForeignKeyField("models.Spot", related_name="devices")
    status = fields.CharEnumField(
        enum_type=DeviceStatus,
        description="Status do dispositivo"
    )
    chip_id = fields.CharField(max_length=50, unique=True)
    last_communication = fields.DatetimeField(null=True)

    class Meta:
        table = "dispositivos"
        ordering = ["id"]

    def __str__(self):
        return f"{self.chip_id} - {self.status}"