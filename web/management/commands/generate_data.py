import random
from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from web.models import TimeSlot, User, TimeSlotTag


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = now()
        user = User.objects.first()
        tags = TimeSlotTag.objects.filter(user=user)

        time_slots = []

        for day_index in range(30):
            current_date -= timedelta(days=1)

            for slot_index in range(randint(5, 10)):
                start_date = current_date + timedelta(hours=randint(0, 10))
                end_date = start_date + timedelta(hours=randint(0, 10))

                time_slots.append(TimeSlot(
                    title=f'generated {day_index}-{slot_index}',
                    start_date=start_date,
                    end_date=end_date,
                    is_realtime=random.choice((True, False)),
                    user=user
                ))

        saved_time_slots = TimeSlot.objects.bulk_create(time_slots)
        time_slot_tags = []
        for time_slot in saved_time_slots:
            count_of_tags = randint(0, len(tags))
            for tag_index in range(count_of_tags):
                time_slot_tags.append(
                    TimeSlot.tags.through(timeslot_id=time_slot.id, timeslottag_id=tags[tag_index].id)
                )
        TimeSlot.tags.through.objects.bulk_create(time_slot_tags)
