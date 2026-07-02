from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard),
    path("teacher-dashboard/", views.teacher_dashboard),
    path("student-dashboard/", views.student_dashboard),
    path("parent-dashboard/", views.parent_dashboard),
]