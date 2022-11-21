from django.core.management.base import BaseCommand
from attendance.models import LabAttendanceTb
from django.db.models import Q
from datetime import date, timedelta, datetime, time
from .get_event import get_event_from_calendarIDs

class Command(BaseCommand):
    def handle(self, *args, **options):
        status_reset()
        ####################
        # Googlecalendar連携機能ON
        # update_comment()
        ####################

def status_reset():
    users = LabAttendanceTb.objects.all()

    for i in range(users.count()):
        set_id = users[i].user_id
        result = LabAttendanceTb.objects.get(user_id=set_id)
        result.status = "absent"
        result.update_time = datetime.now()
        result.save()

def update_comment():
    users = LabAttendanceTb.objects.all()
    calendar_ids = []

    for i in range(users.count()):
        set_id = users[i].user_id
        result = LabAttendanceTb.objects.get(user_id=set_id)
        calendar_ids.append(result.calendar_id)
    
    all_today_events = get_event_from_calendarIDs(calendar_ids)

    for i in range(users.count()):
        set_id = users[i].user_id
        result = LabAttendanceTb.objects.get(user_id=set_id)
        result.comment = all_today_events[i]
        result.save()


        