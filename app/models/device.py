from tortoise import fields
from tortoise.models import Model

class Device(Model):
    id = fields.IntField(pk=True)
    parking_spot = fields.ForeignKeyField("models.ParkingSpot", related_name="devices")
    status = fields.CharEnumField(
        enum_type=("active", "inactive", "error"),
        description="Current device state"
    )
    chip_id = fields.CharField(max_length=50, unique=True)
    last_communication = fields.DatetimeField(null=True)

    class Meta:
        table = "device"
        ordering = ["id"]

    def __str__(self):
        return f"{self.chip_id} - {self.status}"
