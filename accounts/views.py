from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache


@never_cache
def login_view(request):

    if request.user.is_authenticated:

        if request.user.user_type == "admin":
            return redirect("/dashboard/admin/")

        elif request.user.user_type == "teacher":
            return redirect("/dashboard/teacher/")

        elif request.user.user_type == "student":
            return redirect("/dashboard/student/")

        elif request.user.user_type == "parent":
            return redirect("/dashboard/parent/")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.user_type == "admin":
                return redirect("/dashboard/admin/")

            elif user.user_type == "teacher":
                return redirect("/dashboard/teacher/")

            elif user.user_type == "student":
                return redirect("/dashboard/student/")

            elif user.user_type == "parent":
                return redirect("/dashboard/parent/")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "accounts/login.html")


@never_cache
def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")