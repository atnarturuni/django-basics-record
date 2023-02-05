from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout

from web.forms import RegistrationForm, AuthForm, TimeSlotForm, TimeSlotTagForm
from web.models import TimeSlot, TimeSlotTag

User = get_user_model()


def main_view(request):
    timeslots = TimeSlot.objects.all()
    return render(request, "web/main.html", {
        'timeslots': timeslots
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form, "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


def time_slot_edit_view(request, id=None):
    timeslot = TimeSlot.objects.get(id=id) if id is not None else None
    form = TimeSlotForm(instance=timeslot)
    if request.method == 'POST':
        form = TimeSlotForm(data=request.POST, files=request.FILES, instance=timeslot, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/time_slot_form.html", {"form": form})


def tags_view(request):
    tags = TimeSlotTag.objects.all()
    form = TimeSlotTagForm()
    if request.method == 'POST':
        form = TimeSlotTagForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            form = TimeSlotTagForm()
    return render(request, "web/tags.html", {"tags": tags, "form": form})
