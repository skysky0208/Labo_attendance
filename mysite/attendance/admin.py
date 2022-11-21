from django.contrib import admin
from .models import LabAttendanceTb

from .models import LabFingerprintTb
from .models import LabTips
from .models import LabReport
# Register your models here.

# admin画面
admin.site.register(LabAttendanceTb)
admin.site.register(LabFingerprintTb)
admin.site.register(LabTips)
admin.site.register(LabReport)

