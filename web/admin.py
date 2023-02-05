from django.contrib import admin

from web.models import TimeSlot


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date', 'get_spent_time')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_spent_time()

    @admin.display(description='Потраченное время')
    def get_spent_time(self, instance):
        return instance.spent_time


admin.site.register(TimeSlot, TimeSlotAdmin)
