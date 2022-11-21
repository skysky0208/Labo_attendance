from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserCreateForm
from .forms import CommentUpdateForm
from .forms import SearchForm
from .forms import FingerprintCreateForm
from .models import LabAttendanceTb
from .models import LabFingerprintTb
from .models import LabTips
from django.db.models import Q
import random
import json
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import date,timedelta

# Create your views here.
# どのhtmlで出力するかの指定
# 出席情報画面
class AttendanceListView(generic.ListView):
    model = LabAttendanceTb
    template_name = 'attendance/attendance_list.html'


    def get_context_data(self, **kwargs):
        model_list = LabAttendanceTb.objects.all()

        tips_list = LabTips.objects.all()
        tips_size = tips_list.count()
        random_num = random.randint(1, tips_size)

        query = LabTips.objects.get(pk = random_num)

        context = {
            'labattendancetb_list': model_list,
            'image_name': "img/" + query.image,
            'text': query.sentence,
        }
        return context


# ユーザ登録画面
class UserCreateView(generic.CreateView):
    model = LabAttendanceTb
    form_class = UserCreateForm
    template_name = 'attendance/user_create.html'
    # ユーザ作成成功時のリダイレクト先
    success_url = reverse_lazy('attendance:attendance_list')

# 指紋登録画面
class FingerprintCreateView(generic.CreateView):
    model = LabFingerprintTb
    form_class = FingerprintCreateForm
    template_name = 'attendance/fingerprint_create.html'
    # ユーザ作成成功時のリダイレクト先
    success_url = reverse_lazy('attendance:attendance_list')

# コメント編集画面
class CommentUpdateView(generic.UpdateView): 
    model = LabAttendanceTb
    form_class = CommentUpdateForm
    template_name = 'attendance/comment_update.html'
    # ユーザ作成成功時のリダイレクト先
    success_url = reverse_lazy('attendance:attendance_list')

# 検索画面
class SearchView(generic.ListView):
    template_name = 'attendance/search.html'
    model = LabAttendanceTb

    paginate_by = 5
    
    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('user_id', None),
            self.request.POST.get('user_name', None),
            self.request.POST.get('status', None),
        ]
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        user_id = ''
        user_name = ''
        status = ''

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            user_id = form_value[0]
            user_name = form_value[1]
            status = form_value[2]
        default_data = {'user_id': user_id, 
                        'user_name': user_name,
                        'status': status,  
                        }
        test_form = SearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form
        return context

    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            user_id = form_value[0]
            user_name = form_value[1]
            status = form_value[2]
            # 検索条件
            condition_user_id = Q()
            condition_user_name = Q()
            condition_status = Q()
            if len(user_id) != 0 and user_id[0]:
                condition_user_id = Q(user_id__contains=user_id)
            if len(user_name) != 0 and user_name[0]:
                condition_user_name = Q(user_name__icontains=user_name)
            if len(status) != 0 and status[0]:
                condition_status = Q(status__icontains=status)
            return LabAttendanceTb.objects.select_related().filter(condition_user_id & condition_user_name & condition_status )
        else:
            # 何も返さない
            return LabAttendanceTb.objects.none()
