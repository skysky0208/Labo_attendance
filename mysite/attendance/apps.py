from django.apps import AppConfig

# 'oython3 manage.py runserver'コマンドによる実行プロセス

class AttendanceConfig(AppConfig):
    name = 'attendance'

    def ready(self):
        from . import signals