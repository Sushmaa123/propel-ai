from django.contrib import admin
from .models import Feeder, DistributionTransformer, Pole, Device

admin.site.register(Feeder)
admin.site.register(DistributionTransformer)
admin.site.register(Pole)
admin.site.register(Device)