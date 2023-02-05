from django.contrib import admin

from web.models import TimeSlot


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', "user", 'start_date', 'end_date', 'get_spent_time')
    search_fields = ("id", "title")
    list_filter = ("start_date", "end_date", "is_realtime")
    ordering = ('-start_date',)
    readonly_fields = ('is_realtime',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_spent_time()

    @admin.display(description='Потраченное время')
    def get_spent_time(self, instance):
        return instance.spent_time


admin.site.register(TimeSlot, TimeSlotAdmin)
