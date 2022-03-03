from django.test import TestCase
from django.urls import reverse, resolve
from ..views import AttendanceListView

class TestUrls(TestCase):

  def test_attendance_list_url(self):
    view = resolve('/attendance/attendance_list')
    self.assertEqual(view.func.view_class, AttendanceListView)