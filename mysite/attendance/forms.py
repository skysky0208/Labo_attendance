from django import forms
from .models import LabAttendanceTb
from .models import LabFingerprintTb

# 入力画面に関するクラスを定義

# ユーザ登録フォーム
class UserCreateForm(forms.ModelForm):

    class Meta:
        model = LabAttendanceTb
        # 入力するカラムを指定
        fields = ('user_id', 'user_name', 'room_id', 'mail' , 'calendar_id') 

# 指紋登録フォーム
class FingerprintCreateForm(forms.ModelForm):

    class Meta:
        model = LabFingerprintTb
        # 入力するカラムを指定
        fields = ('finger_id', 'user_id')

# コメント編集フォーム
class CommentUpdateForm(forms.ModelForm):

    class Meta:
        model = LabAttendanceTb
        # 入力するカラムを指定
        fields = ('comment',) 

# 検索フォーム
class SearchForm(forms.Form):

    STATUS_CHOICES = (
        ('', ''),
        ('attend', '出席'),
        ('absent', '退席'),
        ('lab out', '外出'),
    )

    user_id = forms.IntegerField(
        initial='',
        label='学籍番号',
        required = False, # 必須ではない
    )

    user_name = forms.CharField(
        initial='',
        label='名前',
        required = False, # 必須ではない
    )

    status = forms.fields.ChoiceField(
        choices=STATUS_CHOICES,
        label='出席状況',
        required = False,  # 必須ではない
    )
    
