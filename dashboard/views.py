from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from datetime import date
from django.db.models import Sum, Count

from students.models import Student
from teachers.models import Teacher
from parents.models import Parent
from classes.models import SchoolClass
from attendance.models import Attendance
from fees.models import Fee
from subjects.models import Subject
from examinations.models import Examination
from announcements.models import Announcement


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("/accounts/login/")

            if request.user.user_type != role:
                return redirect("/accounts/login/")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


@login_required
@role_required("admin")
def admin_dashboard(request):

    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_parents = Parent.objects.count()
    total_classes = SchoolClass.objects.count()
    total_subjects = Subject.objects.count()

    total_fee_records = Fee.objects.count()

    total_fees_collected = (
        Fee.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
    )

    total_fee_amount = (
        Fee.objects.aggregate(total=Sum("amount"))["total"] or 0
    )

    outstanding_balance = total_fee_amount - total_fees_collected

    today = date.today()

    present_today = Attendance.objects.filter(
        date=today,
        status="Present"
    ).count()

    absent_today = Attendance.objects.filter(
        date=today,
        status="Absent"
    ).count()

    late_today = Attendance.objects.filter(
        date=today,
        status="Late"
    ).count()

    class_data = (
        SchoolClass.objects
        .annotate(total_students=Count("student"))
        .order_by("class_name")
    )

    class_labels = [c.class_name for c in class_data]
    class_totals = [c.total_students for c in class_data]

    grade_data = (
        Examination.objects
        .values("grade")
        .annotate(total=Count("id"))
        .order_by("grade")
    )

    grade_labels = [g["grade"] for g in grade_data]
    grade_totals = [g["total"] for g in grade_data]

    latest_announcements = Announcement.objects.order_by("-created_at")[:5]

    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_parents": total_parents,
        "total_classes": total_classes,
        "total_subjects": total_subjects,

        "present_today": present_today,
        "absent_today": absent_today,
        "late_today": late_today,

        "total_fee_records": total_fee_records,
        "total_fees_collected": total_fees_collected,
        "outstanding_balance": outstanding_balance,

        "latest_announcements": latest_announcements,

        "class_labels": class_labels,
        "class_totals": class_totals,

        "grade_labels": grade_labels,
        "grade_totals": grade_totals,
    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context,
    )


@login_required
@role_required("teacher")
def teacher_dashboard(request):

    return render(
        request,
        "dashboard/admin_dashboard.html",
        {
            "total_students": Student.objects.count(),
            "total_teachers": Teacher.objects.count(),
            "total_parents": Parent.objects.count(),
            "total_classes": SchoolClass.objects.count(),
            "total_subjects": Subject.objects.count(),

            "present_today": Attendance.objects.filter(
                date=date.today(),
                status="Present"
            ).count(),

            "absent_today": Attendance.objects.filter(
                date=date.today(),
                status="Absent"
            ).count(),

            "late_today": Attendance.objects.filter(
                date=date.today(),
                status="Late"
            ).count(),

            "total_fee_records": Fee.objects.count(),

            "latest_announcements": Announcement.objects.order_by("-created_at")[:5],

            "class_labels": [],
            "class_totals": [],
            "grade_labels": [],
            "grade_totals": [],
        }
    )


@login_required
@role_required("student")
def student_dashboard(request):
    return render(
        request,
        "dashboard/student_dashboard.html"
    )


@login_required
@role_required("parent")
def parent_dashboard(request):
    return render(
        request,
        "dashboard/parent_dashboard.html"
    )