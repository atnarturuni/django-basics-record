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
