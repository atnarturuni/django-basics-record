import csv


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

