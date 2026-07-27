from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Subject
from .forms import SubjectForm


def subject_list(request):

    search = request.GET.get("search", "").strip()

    subjects = Subject.objects.select_related(
        "teacher"
    ).order_by(
        "subject_name"
    )

    if search:
        subjects = subjects.filter(
            subject_name__icontains=search
        )

    return render(
        request,
        "subjects/subject_list.html",
        {
            "subjects": subjects,
            "search": search,
        },
    )


def add_subject(request):

    if request.method == "POST":

        form = SubjectForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Subject added successfully."
            )

            return redirect("subject-list")

    else:

        form = SubjectForm()

    return render(
        request,
        "subjects/add_subject.html",
        {
            "form": form,
        },
    )


def edit_subject(request, id):

    subject = get_object_or_404(
        Subject,
        id=id
    )

    if request.method == "POST":

        form = SubjectForm(
            request.POST,
            instance=subject
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Subject updated successfully."
            )

            return redirect("subject-list")

    else:

        form = SubjectForm(instance=subject)

    return render(
        request,
        "subjects/edit_subject.html",
        {
            "form": form,
        },
    )


def delete_subject(request, id):

    subject = get_object_or_404(
        Subject,
        id=id
    )

    if request.method == "POST":

        subject.delete()

        messages.success(
            request,
            "Subject deleted successfully."
        )

        return redirect("subject-list")

    return render(
        request,
        "subjects/delete_subject.html",
        {
            "subject": subject,
        },
    )