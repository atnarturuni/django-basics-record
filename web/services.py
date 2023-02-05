import csv

from timetracker.redis import get_redis_client
from web.models import TimeSlot, TimeSlotTag


def filter_timeslots(timeslots_qs, filters: dict):
    if filters['search']:
        timeslots_qs = timeslots_qs.filter(title__icontains=filters['search'])

    if filters['is_realtime'] is not None:
        timeslots_qs = timeslots_qs.filter(is_realtime=filters['is_realtime'])

    if filters['start_date']:
        timeslots_qs = timeslots_qs.filter(start_date__gte=filters['start_date'])

    if filters['end_date']:
        timeslots_qs = timeslots_qs.filter(end_date__lte=filters['end_date'])
    return timeslots_qs


def export_timeslots_csv(timeslots_qs, response):
    writer = csv.writer(response)
    writer.writerow(("title", "start_date", "end_date", "is_realtime", "tags", "spent_time"))

    for timeslot in timeslots_qs:
        writer.writerow((
            timeslot.title, timeslot.start_date, timeslot.end_date, timeslot.is_realtime,
            " ".join([t.title for t in timeslot.tags.all()]),
            timeslot.spent_time
        ))

    return response


def import_timeslots_from_csv(file, user_id):
    strs_from_file = (row.decode() for row in file)
    reader = csv.DictReader(strs_from_file)

    timeslots = []
    timeslot_tags = []
    for row in reader:
        timeslots.append(TimeSlot(
            title=row['title'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            is_realtime=row['is_realtime'],
            user_id=user_id
        ))
        timeslot_tags.append(row['tags'].split(" ") if row['tags'] else [])

    saved_timeslots = TimeSlot.objects.bulk_create(timeslots)

    tags_map = dict(TimeSlotTag.objects.all().values_list("title", "id"))
    time_slot_tags = []
    for timeslot, timeslot_tags_item in zip(saved_timeslots, timeslot_tags):
        for tag in timeslot_tags_item:
            tag_id = tags_map[tag]
            time_slot_tags.append(
                TimeSlot.tags.through(timeslot_id=timeslot.id, timeslottag_id=tag_id)
            )
    TimeSlot.tags.through.objects.bulk_create(time_slot_tags)


def get_stat():
    redis = get_redis_client()
    keys = redis.keys("stat_*")
    return [
        (key.decode().replace("stat_", ""), redis.get(key).decode())
        for key in keys
    ]
