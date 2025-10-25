from tortoise import fields
from tortoise.models import Model

class ParkingSpot(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)

    class Meta:
        table = "parking_spot"
        ordering = ["id"]

    def __str__(self):
        return self.name
