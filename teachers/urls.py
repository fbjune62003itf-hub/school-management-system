from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher_list, name="teacher-list"),
    path("add/", views.add_teacher, name="add-teacher"),
    path("edit/<int:id>/", views.edit_teacher, name="edit-teacher"),
    path("delete/<int:id>/", views.delete_teacher, name="delete-teacher"),
]