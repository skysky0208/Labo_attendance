from django import forms
from .models import LabAttendanceTb

class UserCreateForm(forms.ModelForm):

    class Meta:
        model = LabAttendanceTb
        # 入力するカラムを指定
        fields = ('user_id', 'user_name', 'room_id') 