from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models import Count, F, Max, Min, Q, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from web.forms import RegistrationForm, AuthForm, TimeSlotForm, TimeSlotTagForm, HolidayForm, TimeSlotFilterForm, \
    ImportForm
from web.models import TimeSlot, TimeSlotTag, Holiday
from web.services import filter_timeslots, export_timeslots_csv, import_timeslots_from_csv, get_stat

User = get_user_model()


@cache_page(60)
@login_required
def main_view(request):
    timeslots = TimeSlot.objects.filter(user=request.user).order_by('-start_date')
    current_timeslot = timeslots.filter(end_date__isnull=True).first()

    filter_form = TimeSlotFilterForm(request.GET)
    filter_form.is_valid()
    timeslots = filter_timeslots(timeslots, filter_form.cleaned_data)

    total_count = timeslots.count()
    timeslots = (
        timeslots
        .prefetch_related("tags")
        .select_related("user")
        .annotate(tags_count=Count("tags"))
        .annotate_spent_time()
    )
    page_number = request.GET.get("page", 1)

    paginator = Paginator(timeslots, per_page=100)

    if request.GET.get("export") == 'csv':
        response = HttpResponse(
            content_type='text/csv',
            headers={"Content-Disposition": "attachment; filename=timeslots.csv"}
        )
        return export_timeslots_csv(timeslots, response)

    return render(request, "web/main.html", {
        "current_timeslot": current_timeslot,
        'timeslots': paginator.get_page(page_number),
        "form": TimeSlotForm(),
        "filter_form": filter_form,
        'total_count': total_count
    })


@login_required
def import_view(request):
    if request.method == 'POST':
        form = ImportForm(files=request.FILES)
        if form.is_valid():
            import_timeslots_from_csv(form.cleaned_data['file'], request.user.id)
            return redirect("main")
    return render(request, "web/import.html", {
        "form": ImportForm()
    })


@login_required
def stat_view(request):
    return render(request, "web/stat.html", {"results": get_stat()})



@login_required
def analytics_view(request):
    overall_stat = TimeSlot.objects.aggregate(
        count=Count("id"),
        max_date=Max("end_date"),
        min_date=Min("start_date")
    )
    days_stat = (
        TimeSlot.objects.exclude(end_date__isnull=True)
        .annotate(date=TruncDate("start_date"))
        .values("date")
        .annotate(
            count=Count("id"),
            realtime_count=Count("id", filter=Q(is_realtime=True)),
            spent_time=Sum(F("end_date") - F("start_date"))
        )
        .order_by('-date')
    )

    return render(request, "web/analytics.html", {
        "overall_stat": overall_stat,
        'days_stat': days_stat
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


@login_required
def time_slot_edit_view(request, id=None):
    timeslot = get_object_or_404(TimeSlot, user=request.user, id=id) if id is not None else None
    form = TimeSlotForm(instance=timeslot)
    if request.method == 'POST':
        form = TimeSlotForm(data=request.POST, files=request.FILES, instance=timeslot, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/time_slot_form.html", {"form": form})


@login_required
def time_slot_stop_view(request, id):
    if request.method == 'POST':
        timeslot = get_object_or_404(TimeSlot, user=request.user, id=id)
        timeslot.end_date = now()
        timeslot.save()
    return redirect('main')


@login_required
def time_slot_delete_view(request, id):
    tag = get_object_or_404(TimeSlot, user=request.user, id=id)
    tag.delete()
    return redirect('main')


def _list_editor_view(request, model_cls, form_cls, template_name, url_name):
    items = model_cls.objects.filter(user=request.user)
    form = form_cls()
    if request.method == 'POST':
        form = form_cls(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect(url_name)
    return render(request, f"web/{template_name}.html", {"items": items, "form": form})


@login_required
def tags_view(request):
    return _list_editor_view(request, TimeSlotTag, TimeSlotTagForm, "tags", "tags")


@login_required
def tags_delete_view(request, id):
    tag = get_object_or_404(TimeSlotTag, user=request.user, id=id)
    tag.delete()
    return redirect('tags')


@login_required
def holidays_view(request):
    return _list_editor_view(request, Holiday, HolidayForm, "holidays", "holidays")


@login_required
def holidays_delete_view(request, id):
    holiday = get_object_or_404(Holiday, user=request.user, id=id)
    holiday.delete()
    return redirect('holiday')
