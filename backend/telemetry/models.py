from django.db import models
from network.models import Device


class Telemetry(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="telemetry"
    )

    event = models.CharField(max_length=50)

    energized = models.BooleanField()

    timestamp = models.DateTimeField(auto_now_add=True)

    sequence_number = models.IntegerField(default=0)

    battery_mv = models.IntegerField(default=0)

    rssi = models.IntegerField(default=0)

    firmware = models.CharField(max_length=20, default="1.0.0")

    def __str__(self):
        return f"{self.device.device_id} - {self.event}"