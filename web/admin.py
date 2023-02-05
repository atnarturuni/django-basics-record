from django.contrib import admin

from web.models import TimeSlot


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date')


admin.site.register(TimeSlot, TimeSlotAdmin)
