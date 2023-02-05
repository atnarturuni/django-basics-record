from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import F, Sum

User = get_user_model()


class TimeSlotTag(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class TimeSlotQuerySet(models.QuerySet):
    def annotate_spent_time(self):
        return self.annotate(spent_time=F("end_date") - F("start_date"))


class TimeSlot(models.Model):
    objects = TimeSlotQuerySet.as_manager()

    title = models.CharField(max_length=256, verbose_name='Название')
    start_date = models.DateTimeField(verbose_name='Время начала', default=timezone.now)
    end_date = models.DateTimeField(verbose_name='Время окончания', null=True, blank=True)
    is_realtime = models.BooleanField(default=False, verbose_name='В реальном времени')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tags = models.ManyToManyField(TimeSlotTag, verbose_name='Теги', blank=True)
    image = models.ImageField(upload_to='time_slots/', null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'слот'
        verbose_name_plural = 'слоты'


class Holiday(models.Model):
    date = models.DateField(verbose_name='Дата')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
