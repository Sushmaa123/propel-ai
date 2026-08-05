from rest_framework import serializers
from .models import Pole


class PoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pole
        fields = "__all__"