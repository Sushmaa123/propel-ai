from django.core.management.base import BaseCommand

from network.models import (
    Feeder,
    DistributionTransformer,
    Pole,
    Device,
)

from incidents.models import Incident, Ticket


class Command(BaseCommand):
    help = "Seed sample data"

    def handle(self, *args, **kwargs):

        Ticket.objects.all().delete()
        Incident.objects.all().delete()
        Device.objects.all().delete()
        Pole.objects.all().delete()
        DistributionTransformer.objects.all().delete()
        Feeder.objects.all().delete()

        feeder = Feeder.objects.create(
            feeder_id="FD001",
            name="Main Feeder"
        )

        transformer = DistributionTransformer.objects.create(
            transformer_id="DT001",
            name="Transformer 1",
            feeder=feeder
        )

        poles = []

        for i in range(1, 6):
            pole = Pole.objects.create(
                pole_id=f"P00{i}",
                sequence_number=i,
                latitude=12.90 + i * 0.001,
                longitude=77.50 + i * 0.001,
                transformer=transformer
            )

            Device.objects.create(
                device_id=f"D00{i}",
                pole=pole
            )

            poles.append(pole)

        incident = Incident.objects.create(
            incident_id="INC-001",
            start_pole=poles[1],
            end_pole=poles[3],
            confidence=0.94,
            status="DETECTED"
        )

        Ticket.objects.create(
            ticket_number="TKT-001",
            incident=incident,
            assigned_to="Crew A",
            status="ASSIGNED"
        )

        self.stdout.write(
            self.style.SUCCESS("Seed data created successfully.")
        )