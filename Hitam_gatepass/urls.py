from django.urls import path
from . import views

app_name = 'Hitam_gatepass'

urlpatterns = [
    path('', views.index, name='index'),
    path('Student_enter/', views.Student_enter, name='Student_enter'),
    path('Student/', views.Student, name='student'),
    path('Normal_pass/', views.Normal_pass, name='Normal_pass'),
    path('Emergency_pass/', views.Emergency_pass, name='Emergency_pass'),
    path('apply-pass/', views.apply_gatepass, name='apply_gatepass'),
    path('faculty/', views.Faculty_enter, name='faculty'),
    path('hod-approve/<int:gatepass_id>/', views.hod_approve_gatepass, name='hod_approve_gatepass'),
    path('normal-pass-approve/<int:gatepass_id>/', views.normal_approve_gatepass, name='normal_approve_gatepass'),
    path('mentor-approve/<int:gatepass_id>/', views.mentor_approve_gatepass, name='mentor_approve_gatepass'),
    path('approve-pass/', views.get_gatepasses, name='approve_gatepass'),
]