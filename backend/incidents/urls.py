from django.urls import path
from .views import incident_list, ticket_list, incident_summary,update_ticket_status
urlpatterns = [
    path("incidents/", incident_list),
    path("tickets/", ticket_list),
    path("incidents/<str:incident_id>/summary/", incident_summary),
    path("tickets/<str:ticket_number>/status/",update_ticket_status),
]