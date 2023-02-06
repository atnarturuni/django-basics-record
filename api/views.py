from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def main_view(request):
    return JsonResponse({"status": "ok"})
