from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Parent
from .forms import ParentForm


def parent_list(request):
    search = request.GET.get("search")

    if search:
        parents = Parent.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    else:
        parents = Parent.objects.all()

    return render(request, "parents/parents_list.html", {
        "parents": parents
    })


def add_parent(request):
    if request.method == "POST":
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("parent-list")
    else:
        form = ParentForm()

    return render(request, "parents/add_parent.html", {
        "form": form
    })


def edit_parent(request, id):
    parent = get_object_or_404(Parent, id=id)

    if request.method == "POST":
        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            return redirect("parent-list")
    else:
        form = ParentForm(instance=parent)

    return render(request, "parents/edit_parent.html", {
        "form": form
    })


def delete_parent(request, id):
    parent = get_object_or_404(Parent, id=id)

    if request.method == "POST":
        parent.delete()
        return redirect("parent-list")

    return render(request, "parents/delete_parent.html", {
        "parent": parent
    })