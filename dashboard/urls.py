from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="dashboard"),

    path("admin/", views.admin_dashboard, name="admin-dashboard"),
    path("teacher/", views.teacher_dashboard, name="teacher-dashboard"),
    path("student/", views.student_dashboard, name="student-dashboard"),
    path("parent/", views.parent_dashboard, name="parent-dashboard"),
]