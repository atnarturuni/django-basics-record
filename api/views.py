from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.serializers import TimeSlotSerializer
from web.models import TimeSlot


@api_view(["GET"])
@permission_classes([])
def main_view(request):
    return Response({"status": "ok"})


@api_view(["GET", "POST"])
def timeslots_view(request):
    if request.method == 'POST':
        serializer = TimeSlotSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    time_slots = TimeSlot.objects.all().select_related("user").prefetch_related("tags")
    serializer = TimeSlotSerializer(time_slots, many=True)
    return Response(serializer.data)
