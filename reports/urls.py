from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.report_dashboard,
        name="report-dashboard"
    ),

    path(
        "students/",
        views.student_report,
        name="student-report"
    ),

    path(
        "teachers/",
        views.teacher_report,
        name="teacher-report"
    ),

    path(
        "fees/",
        views.fee_report,
        name="fee-report"
    ),

    path(
        "attendance/",
        views.attendance_report,
        name="attendance-report"
    ),

    path(
        "examinations/",
        views.examination_report,
        name="examination-report"
    ),

    path(
        "examinations/pdf/",
        views.export_exam_pdf,
        name="export-exam-pdf"
    ),

]