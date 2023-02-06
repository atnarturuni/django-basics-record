from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import TimeSlotSerializer
from web.models import TimeSlot


@api_view(["GET"])
def main_view(request):
    return Response({"status": "ok"})


@api_view(["GET"])
def timeslots_view(request):
    time_slots = TimeSlot.objects.all().select_related("user").prefetch_related("tags")
    serializer = TimeSlotSerializer(time_slots, many=True)
    return Response(serializer.data)
