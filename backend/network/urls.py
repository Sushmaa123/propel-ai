from django.urls import path
from .views import get_poles

urlpatterns = [
    path("poles/", get_poles, name="get_poles"),
]