from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.subject_list,
        name="subject-list"
    ),

    path(
        "add/",
        views.add_subject,
        name="add-subject"
    ),

    path(
        "edit/<int:id>/",
        views.edit_subject,
        name="edit-subject"
    ),

    path(
        "delete/<int:id>/",
        views.delete_subject,
        name="delete-subject"
    ),

]