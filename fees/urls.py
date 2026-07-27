from django.urls import path
from . import views

urlpatterns = [

    path("", views.fee_list, name="fee-list"),

    path("add/", views.add_fee, name="add-fee"),

    path("edit/<int:id>/", views.edit_fee, name="edit-fee"),

    path("delete/<int:id>/", views.delete_fee, name="delete-fee"),

]