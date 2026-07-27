from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Student
from .forms import StudentForm


def student_list(request):
    search = request.GET.get("search")

    if search:
        students = Student.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(admission_number__icontains=search)
        )
    else:
        students = Student.objects.all()

    return render(request, "students/student_list.html", {
        "students": students
    })


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-list")
    else:
        form = StudentForm()

    return render(request, "students/add_student.html", {"form": form})


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student-list")
    else:
        form = StudentForm(instance=student)

    return render(request, "students/edit_student.html", {
        "form": form
    })


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("student-list")

    return render(request, "students/delete_student.html", {
        "student": student
    })