from tortoise import fields
from tortoise.models import Model
from enum import Enum

class ReservationStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class SpotState(str, Enum):
    WAITING = "waiting"
    IN_USE = "in_use"
    EMPTY = "empty"

class Reservation(Model):
    id = fields.IntField(pk=True)
    parking_spot = fields.ForeignKeyField("models.Spot", related_name="reservations")
    client = fields.ForeignKeyField("models.Client", related_name="reservations")
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    status = fields.CharEnumField(
        enum_type=ReservationStatus,
        description="Reservation status"
    )
    current_spot_state = fields.CharEnumField(
        enum_type=SpotState,
        description="Current parking spot state"
    )

    class Meta:
        table = "reservas"
        ordering = ["start_time"]

    def __str__(self):
        return f"Reservation {self.id} - {self.status.value}"
