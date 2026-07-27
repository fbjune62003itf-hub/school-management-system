from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Teacher
from .forms import TeacherForm


def teacher_list(request):
    search = request.GET.get("search")

    if search:
        teachers = Teacher.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(employee_number__icontains=search)
        )
    else:
        teachers = Teacher.objects.all()

    return render(request, "teachers/teacher_list.html", {
        "teachers": teachers
    })


def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher-list")
    else:
        form = TeacherForm()

    return render(request, "teachers/add_teacher.html", {"form": form})


def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teacher-list")
    else:
        form = TeacherForm(instance=teacher)

    return render(request, "teachers/edit_teacher.html", {
        "form": form
    })


def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":
        teacher.delete()
        return redirect("teacher-list")

    return render(request, "teachers/delete_teacher.html", {
        "teacher": teacher
    })