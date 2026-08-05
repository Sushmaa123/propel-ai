from django.urls import path
from .views import receive_telemetry

urlpatterns = [
    path("telemetry/", receive_telemetry, name="receive_telemetry"),
]