from django.db import models
from network.models import Pole


class Incident(models.Model):
    STATUS_CHOICES = [
        ("DETECTED", "Detected"),
        ("ACKNOWLEDGED", "Acknowledged"),
        ("ASSIGNED", "Assigned"),
        ("RESOLVED", "Resolved"),
        ("VERIFIED", "Verified"),
        ("CLOSED", "Closed"),
]
    incident_id = models.CharField(max_length=50, unique=True)

    start_pole = models.ForeignKey(
        Pole,
        on_delete=models.CASCADE,
        related_name="incident_start"
    )

    end_pole = models.ForeignKey(
        Pole,
        on_delete=models.CASCADE,
        related_name="incident_end"
    )

    confidence = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DETECTED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.incident_id
class Ticket(models.Model):
    STATUS_CHOICES = [
        ("DETECTED", "Detected"),
        ("ACKNOWLEDGED", "Acknowledged"),
        ("ASSIGNED", "Assigned"),
        ("RESOLVED", "Resolved"),
        ("CLOSED", "Closed"),
    ]

    ticket_number = models.CharField(max_length=50, unique=True)

    incident = models.OneToOneField(
        Incident,
        on_delete=models.CASCADE,
        related_name="ticket"
    )

    assigned_to = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DETECTED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket_number