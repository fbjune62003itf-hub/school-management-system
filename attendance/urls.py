from django.urls import path
from . import views

urlpatterns = [
    path("take/", views.take_attendance, name="take-attendance"),
    path("", views.attendance_list, name="attendance-list"),
    path("add/", views.add_attendance, name="add-attendance"),
    path("edit/<int:id>/", views.edit_attendance, name="edit-attendance"),
    path("delete/<int:id>/", views.delete_attendance, name="delete-attendance"),
]