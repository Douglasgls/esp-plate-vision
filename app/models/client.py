from tortoise import fields
from tortoise.models import Model

class Client(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    cpf = fields.CharField(max_length=20, unique=True)
    phone = fields.CharField(max_length=20, null=True)
    email = fields.CharField(max_length=100, null=True)
    license_plate = fields.CharField(max_length=10, null=True)

    class Meta:
        table = "client"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.cpf})"
