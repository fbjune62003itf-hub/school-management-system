from django.urls import path
from . import views

urlpatterns = [
    path("", views.announcement_list, name="announcement-list"),
    path("add/", views.add_announcement, name="announcement-add"),
    path("edit/<int:pk>/", views.edit_announcement, name="announcement-edit"),
    path("delete/<int:pk>/", views.delete_announcement, name="announcement-delete"),
]