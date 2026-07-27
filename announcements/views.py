from django.shortcuts import render, redirect, get_object_or_404

from .models import Announcement
from .forms import AnnouncementForm


def announcement_list(request):

    announcements = Announcement.objects.all().order_by("-created_at")

    return render(
        request,
        "announcements/announcement_list.html",
        {
            "announcements": announcements,
        },
    )


def add_announcement(request):

    if request.method == "POST":
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("announcement-list")

    else:
        form = AnnouncementForm()

    return render(
        request,
        "announcements/add_announcement.html",
        {
            "form": form,
        },
    )


def edit_announcement(request, pk):

    announcement = get_object_or_404(
        Announcement,
        pk=pk
    )

    if request.method == "POST":

        form = AnnouncementForm(
            request.POST,
            instance=announcement
        )

        if form.is_valid():
            form.save()
            return redirect("announcement-list")

    else:

        form = AnnouncementForm(
            instance=announcement
        )

    return render(
        request,
        "announcements/edit_announcement.html",
        {
            "form": form,
        },
    )


def delete_announcement(request, pk):

    announcement = get_object_or_404(
        Announcement,
        pk=pk
    )

    if request.method == "POST":
        announcement.delete()
        return redirect("announcement-list")

    return render(
        request,
        "announcements/delete_announcement.html",
        {
            "announcement": announcement,
        },
    )