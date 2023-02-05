from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, time_slot_edit_view, tags_view, \
    tags_delete_view, holidays_delete_view, holidays_view, time_slot_delete_view, time_slot_stop_view, analytics_view, \
    import_view, stat_view

urlpatterns = [
    path("", main_view, name="main"),
    path("import/", import_view, name="import"),
    path("analytics/", analytics_view, name="analytics"),
    path("stat/", stat_view, name="stat"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("time_slots/add/", time_slot_edit_view, name="time_slots_add"),
    path("time_slots/<int:id>/", time_slot_edit_view, name="time_slots_edit"),
    path("time_slots/<int:id>/delete/", time_slot_delete_view, name="time_slots_delete"),
    path("time_slots/<int:id>/stop/", time_slot_stop_view, name="time_slots_stop"),
    path("tags/", tags_view, name="tags"),
    path("tags/<int:id>/delete/", tags_delete_view, name="tags_delete"),
    path("holidays/", holidays_view, name="holidays"),
    path("holidays/<int:id>/delete/", holidays_delete_view, name="holidays_delete")
]
