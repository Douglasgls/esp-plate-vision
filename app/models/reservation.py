from tortoise import fields
from tortoise.models import Model

class Reservation(Model):
    id = fields.IntField(pk=True)
    parking_spot = fields.ForeignKeyField("models.ParkingSpot", related_name="reservations")
    client = fields.ForeignKeyField("models.Client", related_name="reservations")
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    status = fields.CharEnumField(
        enum_type=("active", "completed", "cancelled"),
        description="Reservation status"
    )
    current_spot_state = fields.CharEnumField(
        enum_type=("waiting", "in_use", "empty"),
        description="Current parking spot state"
    )

    class Meta:
        table = "reservation"
        ordering = ["start_time"]

    def __str__(self):
        return f"Reservation {self.id} - {self.status}"
