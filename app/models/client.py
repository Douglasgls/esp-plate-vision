from tortoise import fields
from tortoise.models import Model


class Client(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=100)
    cpf = fields.CharField(max_length=20, unique=True)
    phone_number = fields.CharField(max_length=20, null=True)
    email_address = fields.CharField(max_length=100, null=True)
    license_plate = fields.CharField(max_length=10, null=True)

    class Meta:
        table = "Clientes"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.cpf})"
