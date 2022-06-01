from attendance.models import LabReport
from attendance.models import LabAttendanceTb
from django.db.models import Q
from datetime import date, timedelta, datetime, time

def get_h_m(td):
    h, m = divmod(td, 60)
    return int(h), int(m)

def get_data(report_data, userid, rangeday):

    search_datetime = datetime.now() - timedelta(days = rangeday)
    search_date = search_datetime.date()

    data_list = []
    date_list = []
    enter_time_list = []
    stay_time_list = []
    

    for i in range(5):
        today_report = report_data.filter(
            date = search_date,
            student_id = userid
        )

        if today_report.count() != 0:
            data_dict = {}
            stay_hour, stay_minute = get_h_m(today_report[0].staytime)

            date_list.append(search_date)
            enter_time_list.append(today_report[0].enter_time)
            stay_time_list.append(today_report[0].staytime)

            data_dict['date'] = str(search_date.year) + "年" + str(search_date.month) + "月" + str(search_date.day) + "日"
            data_dict['enter_time'] =  str(today_report[0].enter_time.hour) + "時" + str(today_report[0].enter_time.minute) + "分"
            data_dict['stay_time'] =  str(stay_hour) + "時間" + str(stay_minute) + "分"

            data_list.append(data_dict)
        else:
            date_list.append(search_date)
            enter_time_list.append(time(0, 0, 0))
            stay_time_list.append(0)

        search_datetime = search_datetime + timedelta(days=1)
        search_date = search_datetime.date()

    return data_list, date_list, enter_time_list, stay_time_list
