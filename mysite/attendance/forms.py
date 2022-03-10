from django import forms
from .models import LabAttendanceTb

# 入力画面に関するクラスを定義

# ユーザ登録フォーム
class UserCreateForm(forms.ModelForm):

    class Meta:
        model = LabAttendanceTb
        # 入力するカラムを指定
        fields = ('user_id', 'user_name', 'room_id') 

# コメント編集フォーム
class CommentUpdateForm(forms.ModelForm):

    class Meta:
        model = LabAttendanceTb
        # 入力するカラムを指定
        fields = ('comment',) 


