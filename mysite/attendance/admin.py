from django.contrib import admin
from .models import LabAttendanceTb
from .models import LabFingerprintTb
from .models import EnterInfo
from .models import LabTips
# Register your models here.

# admin画面
admin.site.register(LabAttendanceTb)
admin.site.register(LabFingerprintTb)
admin.site.register(EnterInfo)
admin.site.register(LabTips)
