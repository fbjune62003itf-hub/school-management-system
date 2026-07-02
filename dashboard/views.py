from django.shortcuts import render

def admin_dashboard(request):
    return render(request, "dashboard/admin_dashboard.html")

def teacher_dashboard(request):
    return render(request, "dashboard/teacher_dashboard.html")

def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")

def parent_dashboard(request):
    return render(request, "dashboard/parent_dashboard.html")