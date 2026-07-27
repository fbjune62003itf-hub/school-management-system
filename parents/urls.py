from django.urls import path
from . import views

urlpatterns = [
    path("", views.parent_list, name="parent-list"),
    path("add/", views.add_parent, name="add-parent"),
    path("edit/<int:id>/", views.edit_parent, name="edit-parent"),
    path("delete/<int:id>/", views.delete_parent, name="delete-parent"),
]