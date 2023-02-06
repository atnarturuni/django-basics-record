from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import TimeSlotSerializer
from web.models import TimeSlot


@api_view(["GET"])
@permission_classes([])
def main_view(request):
    return Response({"status": "ok"})


class TimeslotModelViewSet(ModelViewSet):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return TimeSlot.objects.all().select_related("user").prefetch_related("tags").filter(user=self.request.user)
