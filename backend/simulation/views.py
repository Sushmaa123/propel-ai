from rest_framework.decorators import api_view
from rest_framework.response import Response

from network.models import Device
from telemetry.models import Telemetry
from incidents.models import Incident, Ticket
from services.fault_localization import localize_fault


@api_view(["POST"])
def inject_fault(request):

    fault_type = request.data.get("fault_type", "span_fault")

    device = Device.objects.get(device_id="D003")

    event = "power_lost"
    energized = False

    # -------------------------
    # Fault Types
    # -------------------------

    if fault_type == "span_fault":
        event = "power_lost"

    elif fault_type == "dt_fault":
        event = "dt_fault"

    elif fault_type == "feeder_fault":
        event = "feeder_fault"

    elif fault_type == "device_failure":
        event = "device_failure"

    elif fault_type == "duplicate_messages":
        event = "duplicate_message"

    elif fault_type == "out_of_order":
        event = "out_of_order"

    elif fault_type == "scheduled_outage":
        event = "scheduled_outage"

    elif fault_type == "repair_fault":
        event = "power_restored"
        energized = True

    telemetry = Telemetry.objects.create(
        device=device,
        event=event,
        energized=energized,
        sequence_number=9999,
        battery_mv=3480,
        rssi=-91,
        firmware="1.4.2"
    )

    # ==========================================
    # Scheduled Outage
    # No Incident should be created
    # ==========================================

    if fault_type == "scheduled_outage":
        return Response({
            "message": "Scheduled outage recorded successfully.",
            "type": "planned_outage"
        })

    # ==========================================
    # Device Failure
    # No outage ticket
    # ==========================================

    if fault_type == "device_failure":
        return Response({
            "message": "Device failure recorded.",
            "type": "device_failure"
        })

    # ==========================================
    # Duplicate Messages
    # Ignore duplicates
    # ==========================================

    if fault_type == "duplicate_messages":
        return Response({
            "message": "Duplicate telemetry ignored."
        })

    # ==========================================
    # Out Of Order
    # Ignore telemetry
    # ==========================================

    if fault_type == "out_of_order":
        return Response({
            "message": "Out-of-order telemetry ignored."
        })

    # ==========================================
    # Repair Fault
    # Verify then Close
    # ==========================================

    if fault_type == "repair_fault":
        Incident.objects.filter(
            status__in=["DETECTED","ACKNOWLEDGED", "CREW_ASSIGNED", "RESOLVED"]
        ).update(status="CLOSED")

        Ticket.objects.filter(
            status__in=["DETECTED", "ACKNOWLEDGED", "ASSIGNED", "RESOLVED"]
        ).update(status="CLOSED")

        return Response({
        "message": "Fault repaired successfully."
        })

    # ==========================================
    # Fault Localization
    # ==========================================

    result = localize_fault()

    if result:

        existing = Incident.objects.filter(
            start_pole=result["start_pole"],
            end_pole=result["end_pole"],
            status="DETECTED"
        ).first()

        if not existing:

            incident = Incident.objects.create(
                incident_id=f"INC-{telemetry.id}",
                start_pole=result["start_pole"],
                end_pole=result["end_pole"],
                confidence=result["confidence"],
                status="DETECTED"
            )

            Ticket.objects.create(
                ticket_number=f"TKT-{telemetry.id}",
                incident=incident,
                status="DETECTED"
            )

    return Response({
        "message": f"{fault_type} injected successfully"
    })