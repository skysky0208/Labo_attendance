from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserCreateForm
from .forms import CommentUpdateForm
from .models import LabAttendanceTb

# Create your views here.
# どのhtmlで出力するかの指定
class IndexView(generic.TemplateView):
    template_name = 'attendance/index.html'

# 出席情報画面
class AttendanceListView(generic.ListView):
    model = LabAttendanceTb
    template_name = 'attendance/attendance_list.html'

# ユーザ登録画面
class UserCreateView(generic.CreateView):
    model = LabAttendanceTb
    form_class = UserCreateForm
    template_name = 'attendance/user_create.html'
    # ユーザ作成成功時のリダイレクト先
    success_url = reverse_lazy('attendance:attendance_list')

# コメント編集画面
class CommentUpdateView(generic.UpdateView): 
    model = LabAttendanceTb
    form_class = CommentUpdateForm
    template_name = 'attendance/comment_update.html'
    # ユーザ作成成功時のリダイレクト先
    success_url = reverse_lazy('attendance:attendance_list')