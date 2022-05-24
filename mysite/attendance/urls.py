from django.urls import path
from . import views

app_name = 'attendance'

# urlの定義
urlpatterns = [
    path('attendance_list', views.AttendanceListView.as_view(), name='attendance_list'),
    path('user_create', views.UserCreateView.as_view(), name='user_create'), 
    path('fingerprint_create', views.FingerprintCreateView.as_view(), name='fingerprint_create'),
    path('search', views.SearchView.as_view(), name='search'), 
    path('comment_update/<int:pk>/', views.CommentUpdateView.as_view(), name='comment_update'),
]