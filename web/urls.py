from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, time_slot_edit_view, tags_view

urlpatterns = [
    path("", main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("time_slots/add/", time_slot_edit_view, name="time_slots_add"),
    path("time_slots/<int:id>/", time_slot_edit_view, name="time_slots_edit"),
    path("tags/", tags_view, name="tags")
]
