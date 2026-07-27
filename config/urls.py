from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect


def home(request):
    return HttpResponseRedirect("/accounts/login/")


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("students/", include("students.urls")),
    path("teachers/", include("teachers.urls")),
    path("parents/", include("parents.urls")),
    path("classes/", include("classes.urls")),
    path("attendance/", include("attendance.urls")),
    path("fees/", include("fees.urls")),
    path("examinations/", include("examinations.urls")),
    path("subjects/", include("subjects.urls")),
    path("reports/", include("reports.urls")),
    path("announcements/", include("announcements.urls")),
]
