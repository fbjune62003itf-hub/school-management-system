from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import SchoolClass
from .forms import SchoolClassForm


def class_list(request):
    search = request.GET.get("search")

    if search:
        classes = SchoolClass.objects.filter(
            Q(class_name__icontains=search) |
            Q(class_teacher__icontains=search)
        )
    else:
        classes = SchoolClass.objects.all()

    return render(request, "classes/class_list.html", {
        "classes": classes
    })


def add_class(request):
    if request.method == "POST":
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("class-list")
    else:
        form = SchoolClassForm()

    return render(request, "classes/add_class.html", {
        "form": form
    })


def edit_class(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)

    if request.method == "POST":
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            return redirect("class-list")
    else:
        form = SchoolClassForm(instance=school_class)

    return render(request, "classes/edit_class.html", {
        "form": form
    })


def delete_class(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)

    if request.method == "POST":
        school_class.delete()
        return redirect("class-list")

    return render(request, "classes/delete_class.html", {
        "school_class": school_class
    })