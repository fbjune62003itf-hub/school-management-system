from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student-list"),
    path("add/", views.add_student, name="add-student"),
    path("edit/<int:id>/", views.edit_student, name="edit-student"),
    path("delete/<int:id>/", views.delete_student, name="delete-student"),
]
