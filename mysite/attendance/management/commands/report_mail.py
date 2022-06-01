from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from attendance.models import LabReport
from attendance.models import LabAttendanceTb
from django.db.models import Q
from datetime import date, timedelta, datetime, time
from .make_graph import make_graph
from .make_report import make_report, avarage_enter_time
from .get_data import get_data, get_h_m


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 今週のデータ抽出
        enddatetime = datetime.now() - timedelta(days=2)
        startdatetime = enddatetime - timedelta(days=5)
        reports = LabReport.objects.filter(date__range=[startdatetime.date(), enddatetime.date()])

        # 先週のデータ抽出
        startdatetime = startdatetime - timedelta(weeks=1)
        enddatetime = enddatetime - timedelta(weeks=1)
        lastweek_reports = LabReport.objects.filter(date__range=[startdatetime.date(), enddatetime.date()])

        users = LabAttendanceTb.objects.all()

        for i in range(users.count()):
            user_address = users[i].mail
            user_id = users[i].user_id

            subject = "今週の研究室出席レポート"

            data, date, enter_time, stay_time = get_data(reports, user_id, 6)
            make_graph(user_id, date, enter_time, stay_time)

            _, _, lastweek_enter_time, lastweek_stay_time = get_data(lastweek_reports, user_id, 13)
            
            context_info = make_report(user_id, date, enter_time, stay_time, lastweek_enter_time, lastweek_stay_time)
            if(len(context_info) == 5):
                context_info.append("100％")

            context = {
                'thisweek_enter': context_info[0],
                'lastweek_enter': context_info[1],
                'enter_ratio': context_info[2],
                'thisweek_stay': context_info[3],
                'lastweek_stay': context_info[4],
                'stay_ratio': context_info[5],
            }
            message = render_to_string('email/report.txt', context)
            from_mail = settings.EMAIL_HOST_USER
            recipient = [user_address]
            bcc = []
            email = EmailMessage(subject, message, from_mail, recipient, bcc)
            email.attach_file('./static/report/' + str(user_id) + '.pdf')
            email.send()