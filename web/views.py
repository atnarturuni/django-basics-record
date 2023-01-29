from datetime import datetime

from django.shortcuts import render

from web.forms import RegistrationForm


def main_view(request):
    year = datetime.now().year
    return render(request, "web/main.html", {
        "year": year
    })


def registration_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    return render(request, "web/registration.html", {"form": form})
