from django.contrib import admin
from .models import Incident, Ticket

admin.site.register(Incident)
admin.site.register(Ticket)