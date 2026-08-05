from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Telemetry
from network.models import Device
from incidents.models import Incident
from services.fault_localization import localize_fault


@api_view(["POST"])
def receive_telemetry(request):
    device_id = request.data.get("device_id")
    event = request.data.get("event")
    energized = request.data.get("energized")
    sequence_number = request.data.get("sequence_number")
    battery_mv = request.data.get("battery_mv")
    rssi = request.data.get("rssi")
    firmware = request.data.get("firmware")

    try:
        device = Device.objects.get(device_id=device_id)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=404)

    telemetry = Telemetry.objects.create(
        device=device,
        event=event,
        energized=energized,
        sequence_number=sequence_number,
        battery_mv=battery_mv,
        rssi=rssi,
        firmware=firmware,
    )

    # Run fault localization only when power is lost
    if not energized:
        result = localize_fault()

        if result:
            # Check if an active incident already exists
            existing_incident = Incident.objects.filter(
                start_pole=result["start_pole"],
                end_pole=result["end_pole"],
                status="DETECTED"
            ).first()

            # Create a new incident only if one doesn't already exist
            if not existing_incident:
                incident = Incident.objects.create(
                    incident_id=f"INC-{telemetry.id}",
                    start_pole=result["start_pole"],
                    end_pole=result["end_pole"],
                    confidence=result["confidence"],
                    status="DETECTED"
                )

                from incidents.models import Ticket

                Ticket.objects.create(
                    ticket_number=f"TKT-{telemetry.id}",
                    incident=incident
                    )

    return Response({
        "message": "Telemetry received",
        "telemetry_id": telemetry.id
    })