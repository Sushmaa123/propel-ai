from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Incident, Ticket
from services.ai_summary import generate_summary


# -------------------------
# Incident List
# -------------------------
@api_view(["GET"])
def incident_list(request):
    incidents = Incident.objects.all().order_by("-created_at")

    data = []

    for incident in incidents:
        data.append({
            "incident_id": incident.incident_id,
            "start_pole": incident.start_pole.pole_id,
            "end_pole": incident.end_pole.pole_id,
            "confidence": incident.confidence,
            "status": incident.status,
        })

    return Response(data)


# -------------------------
# Ticket List
# -------------------------
@api_view(["GET"])
def ticket_list(request):
    tickets = Ticket.objects.all().order_by("-created_at")

    data = []

    for ticket in tickets:
        data.append({
            "ticket_number": ticket.ticket_number,
            "incident": ticket.incident.incident_id,
            "status": ticket.status,
            "assigned_to": ticket.assigned_to,
        })

    return Response(data)


# -------------------------
# AI Incident Summary
# -------------------------
@api_view(["GET"])
def incident_summary(request, incident_id):

    try:
        incident = Incident.objects.get(
            incident_id=incident_id
        )

    except Incident.DoesNotExist:
        return Response(
            {"error": "Incident not found"},
            status=404
        )

    summary = generate_summary(incident)

    return Response({
        "incident_id": incident.incident_id,
        "summary": summary
    })


# -------------------------
# Ticket Workflow
# -------------------------
@api_view(["POST"])
def update_ticket_status(request, ticket_number):

    try:
        ticket = Ticket.objects.get(
            ticket_number=ticket_number
        )

    except Ticket.DoesNotExist:
        return Response(
            {"error": "Ticket not found"},
            status=404
        )

    new_status = request.data.get("status")

    valid_status = [
        "DETECTED",
        "ACKNOWLEDGED",
        "ASSIGNED",
        "RESOLVED",
        "CLOSED",
    ]

    if new_status not in valid_status:
        return Response(
            {"error": "Invalid status"},
            status=400
        )

    # -------------------------
    # Update Ticket
    # -------------------------

    ticket.status = new_status

    if new_status == "ASSIGNED":
        ticket.assigned_to = "Crew A"

    ticket.save()

    # -------------------------
    # Update Incident
    # -------------------------

    incident = ticket.incident

    if new_status == "ACKNOWLEDGED":
        incident.status = "ACKNOWLEDGED"

    elif new_status == "ASSIGNED":
        incident.status = "CREW_ASSIGNED"

    elif new_status == "RESOLVED":
        incident.status = "RESOLVED"

    elif new_status == "CLOSED":
        incident.status = "CLOSED"

    incident.save()

    return Response({
        "message": "Ticket updated successfully",
        "ticket": ticket.ticket_number,
        "ticket_status": ticket.status,
        "incident_status": incident.status
    })