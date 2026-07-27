from django.urls import path
from . import views

urlpatterns = [
    path("", views.class_list, name="class-list"),
    path("add/", views.add_class, name="add-class"),
    path("edit/<int:id>/", views.edit_class, name="edit-class"),
    path("delete/<int:id>/", views.delete_class, name="delete-class"),
]