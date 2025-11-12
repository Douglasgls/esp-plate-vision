from tortoise import fields
from tortoise.models import Model

from app.models.device import Device

class Spot(Model):
    id = fields.IntField(pk=True)
    spot = fields.IntField(max_length=20)
    sector = fields.CharField(max_length=50, null=True)

    class Meta:
        table = "vagas"
        ordering = ["id"]

    def __str__(self):
        return self.name
