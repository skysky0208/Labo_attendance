from django.db import models

# Create your models here.
# DBの定義
class LabAttendanceTb(models.Model):

    ROOM_CHOICES = (
        ('16_321', '16号館321室'),
        ('16_421', '16号館421室'),
        ('16_422', '16号館422室'),
    )

    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    room_id = models.CharField(max_length=100, choices=ROOM_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    calendar_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Lab_attendance_tb'

    # 自分自身を呼び出されたとき学籍番号を返す
    def __str__(self):
        return str(self.user_id)

    @staticmethod
    def get_absolute_url(self):
        return reverse('search:index') 


class LabFingerprintTb(models.Model):
    finger_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Lab_fingerprint_tb'

    def __str__(self):
        return "【"+ str(self.finger_id) + "】　" + str(self.user_id)


class LabAttendanceInfo(models.Model):
    student_id = models.IntegerField()
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    staytime = models.IntegerField(db_column='Staytime', blank=True, null=True) 
    info_count = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'Lab_attendance_info'

    def __str__(self):
        return str(self.info_count)