from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from attendance.models import LabReport
from attendance.models import LabAttendanceTb
from django.db.models import Q
from datetime import date, timedelta, datetime, time

def get_h_m(td):
    h, m = divmod(td, 60)
    return int(h), int(m)

def make_report(report_data, userid):
    report_text = "【今週の出席レポート】\n\n"

    search_datetime = datetime.now() - timedelta(days=5)
    search_date = search_datetime.date()

    for i in range(5):
        today_report = report_data.filter(
            date = search_date,
            student_id = userid
        )

        if today_report.count() != 0:
            stay_hour, stay_minute = get_h_m(today_report[0].staytime)

            today_text = str(search_date.year) + "年" + str(search_date.month) + "月" + str(search_date.day) + "日\n"
            today_text = today_text + "研究室入室時間：" + str(today_report[0].enter_time.hour) + "時" + str(today_report[0].enter_time.minute) + "分\n"
            today_text = today_text + "研究室滞在時間：" + str(stay_hour) + "時間" + str(stay_minute) + "分\n\n"

            report_text = report_text + today_text

        search_datetime = search_datetime + timedelta(days=1)
        search_date = search_datetime.date()

    return report_text


class Command(BaseCommand):

    def handle(self, *args, **options):

        enddatetime = datetime.now() - timedelta(days=1)
        startdatetime = enddatetime - timedelta(days=4)
        reports = LabReport.objects.filter(date__range=[startdatetime.date(), enddatetime.date()])

        users = LabAttendanceTb.objects.all()

        for i in range(users.count()):
            user_address = users[i].mail
            user_id = users[i].user_id

            subject = "今週の研究室出席レポート"
            message = make_report(reports, user_id)
            from_mail = settings.EMAIL_HOST_USER
            recipient = [user_address]
            send_mail(subject, message, from_mail, recipient)