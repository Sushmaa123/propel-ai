from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pole
from .serializers import PoleSerializer


@api_view(["GET"])
def get_poles(request):
    poles = Pole.objects.all()
    serializer = PoleSerializer(poles, many=True)
    return Response(serializer.data)