from datetime import datetime

from django.shortcuts import render


def main_view(request):
    year = datetime.now().year
    return render(request, "web/main.html", {
        "year": year
    })
