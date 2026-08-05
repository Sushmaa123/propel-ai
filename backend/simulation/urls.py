from django.urls import path
from .views import inject_fault

urlpatterns = [
    path("inject-fault/", inject_fault, name="inject_fault"),
]