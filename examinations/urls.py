from django.urls import path
from . import views

urlpatterns = [
    path("", views.exam_list, name="exam-list"),
    path("add/", views.add_exam, name="add-exam"),
    path("edit/<int:id>/", views.edit_exam, name="edit-exam"),
    path("delete/<int:id>/", views.delete_exam, name="delete-exam"),
    path("report/<int:student_id>/", views.report_card, name="report-card"),
]