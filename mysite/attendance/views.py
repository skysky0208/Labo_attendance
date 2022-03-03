from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserCreateForm
from .models import LabAttendanceTb


# Create your views here.
# どのhtmlで出力するかの指定
class IndexView(generic.TemplateView):
    template_name = 'attendance/index.html'

class AttendanceListView(generic.ListView):
    model = LabAttendanceTb
    template_name = 'attendance/attendance_list.html'

class UserCreateView(generic.CreateView):
    model = LabAttendanceTb
    form_class = UserCreateForm
    template_name = 'attendance/user_create.html'
    # ユーザ作成成功時のリダイレクト先
    success_url = reverse_lazy('attendance:attendance_list')