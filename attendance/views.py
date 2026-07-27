from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance
from .forms import AttendanceForm
from classes.models import SchoolClass
from students.models import Student
from django.db.models import Q
from datetime import date


def attendance_list(request):

    classes = SchoolClass.objects.all().order_by("class_name")

    attendance = Attendance.objects.select_related(
        "student",
        "school_class"
    ).order_by("-date", "student__first_name")

    class_id = request.GET.get("class", "")
    attendance_date = request.GET.get("date", "")
    search = request.GET.get("search", "").strip()

    print("SEARCH =", repr(search))

    if class_id:
        attendance = attendance.filter(
            school_class_id=class_id
        )

    if attendance_date:
        attendance = attendance.filter(
            date=attendance_date
        )

    if search:
        attendance = attendance.filter(
        Q(student__first_name__icontains=search) |
        Q(student__last_name__icontains=search) |
        Q(student__admission_number__icontains=search) |
        Q(student__first_name__icontains=search.split()[0])
    )

    # If the user enters both first and last name
    if len(search.split()) > 1:
        attendance = attendance.filter(
            student__first_name__icontains=search.split()[0],
            student__last_name__icontains=search.split()[1]
        )

    print("RESULTS =", attendance.count())

    return render(
        request,
        "attendance/attendance_list.html",
        {
            "attendance": attendance,
            "classes": classes,
            "selected_class": class_id,
            "selected_date": attendance_date,
            "search": search,
        },
    )

def add_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("attendance-list")
    else:
        form = AttendanceForm()

    return render(request, "attendance/add_attendance.html", {
        "form": form
    })


def edit_attendance(request, id):
    record = get_object_or_404(Attendance, id=id)

    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect("attendance-list")
    else:
        form = AttendanceForm(instance=record)

    return render(request, "attendance/edit_attendance.html", {
        "form": form,
    })


def delete_attendance(request, id):
    record = get_object_or_404(Attendance, id=id)

    if request.method == "POST":
        record.delete()
        return redirect("attendance-list")

    return render(request, "attendance/delete_attendance.html", {
        "record": record,
    })


def take_attendance(request):
    classes = SchoolClass.objects.all().order_by("class_name")

    selected_class = None
    students = []

    if request.method == "POST":

        class_id = request.POST.get("class")
        attendance_date = request.POST.get("attendance_date")

        selected_class = get_object_or_404(
            SchoolClass,
            id=class_id
        )

        students = Student.objects.filter(
            school_class=selected_class
        )

        for student in students:

            status = request.POST.get(
                f"status_{student.id}"
            )

            Attendance.objects.update_or_create(

                student=student,
                date=attendance_date,

                defaults={
                    "school_class": selected_class,
                    "status": status,
                }

            )

        return redirect("attendance-list")

    class_id = request.GET.get("class")

    if class_id:

        selected_class = get_object_or_404(
            SchoolClass,
            id=class_id
        )

        students = Student.objects.filter(
            school_class=selected_class
        ).order_by(
            "first_name",
            "last_name"
        )

    return render(
        request,
        "attendance/take_attendance.html",
        {
            "classes": classes,
            "students": students,
            "selected_class": selected_class,
            "today": date.today(),
        },
    )