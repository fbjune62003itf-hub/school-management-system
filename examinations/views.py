from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Value
from django.db.models.functions import Concat

from .models import Examination
from .forms import ExaminationForm
from students.models import Student
from classes.models import SchoolClass


def exam_list(request):

    classes = SchoolClass.objects.all().order_by("class_name")

    terms = [
        "Term 1",
        "Term 2",
        "Term 3",
    ]

    selected_class = request.GET.get("class", "")
    selected_term = request.GET.get("term", "")
    selected_year = request.GET.get("year", "").strip()
    search = request.GET.get("search", "").strip()

    exams = (
        Examination.objects.select_related(
            "student",
            "school_class"
        )
        .annotate(
            full_name=Concat(
                "student__first_name",
                Value(" "),
                "student__last_name",
            )
        )
        .order_by(
            "-academic_year",
            "school_class__class_name",
            "student__first_name",
            "subject",
        )
    )

    if selected_class:
        exams = exams.filter(school_class_id=selected_class)

    if selected_term:
        exams = exams.filter(term=selected_term)

    if selected_year:
        exams = exams.filter(academic_year__icontains=selected_year)

    if search:
        exams = exams.filter(
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(full_name__icontains=search) |
            Q(student__admission_number__icontains=search)
        )

    return render(
        request,
        "examinations/exam_list.html",
        {
            "exams": exams,
            "classes": classes,
            "terms": terms,
            "selected_class": selected_class,
            "selected_term": selected_term,
            "selected_year": selected_year,
            "search": search,
        },
    )


def add_exam(request):

    if request.method == "POST":

        form = ExaminationForm(request.POST)

        if form.is_valid():

            school_class = form.cleaned_data["school_class"]
            student_name = form.cleaned_data["student_name"].strip()

            student = Student.objects.filter(
                school_class=school_class
            ).filter(
                Q(first_name__iexact=student_name) |
                Q(last_name__iexact=student_name) |
                Q(first_name__iexact=student_name.split()[0])
            ).first()

            if student is None:

                parts = student_name.split()

                if len(parts) >= 2:

                    first = parts[0]
                    last = " ".join(parts[1:])

                    student = Student.objects.filter(
                        school_class=school_class,
                        first_name__iexact=first,
                        last_name__iexact=last,
                    ).first()

            if student is None:

                form.add_error(
                    "student_name",
                    "Student not found in the selected class."
                )

            else:

                exam = form.save(commit=False)
                exam.student = student
                exam.save()

                messages.success(
                    request,
                    "Examination result saved successfully."
                )

                return redirect("exam-list")

    else:

        form = ExaminationForm()

    return render(
        request,
        "examinations/add_exam.html",
        {
            "form": form,
        },
    )


def edit_exam(request, id):

    exam = get_object_or_404(
        Examination,
        id=id
    )

    if request.method == "POST":

        form = ExaminationForm(
            request.POST,
            instance=exam
        )

        if form.is_valid():

            school_class = form.cleaned_data["school_class"]
            student_name = form.cleaned_data["student_name"].strip()

            student = Student.objects.filter(
                school_class=school_class
            ).filter(
                Q(first_name__iexact=student_name) |
                Q(last_name__iexact=student_name)
            ).first()

            if student is None:

                parts = student_name.split()

                if len(parts) >= 2:

                    first = parts[0]
                    last = " ".join(parts[1:])

                    student = Student.objects.filter(
                        school_class=school_class,
                        first_name__iexact=first,
                        last_name__iexact=last,
                    ).first()

            if student is None:

                form.add_error(
                    "student_name",
                    "Student not found in the selected class."
                )

            else:

                exam = form.save(commit=False)
                exam.student = student
                exam.save()

                messages.success(
                    request,
                    "Result updated successfully."
                )

                return redirect("exam-list")

    else:

        form = ExaminationForm(
            instance=exam,
            initial={
                "student_name": f"{exam.student.first_name} {exam.student.last_name}"
            }
        )

    return render(
        request,
        "examinations/edit_exam.html",
        {
            "form": form,
        },
    )


def delete_exam(request, id):

    exam = get_object_or_404(
        Examination,
        id=id
    )

    if request.method == "POST":

        exam.delete()

        messages.success(
            request,
            "Result deleted successfully."
        )

        return redirect("exam-list")

    return render(
        request,
        "examinations/delete_exam.html",
        {
            "exam": exam,
        },
    )


def report_card(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    results = Examination.objects.filter(
        student=student
    ).order_by(
        "subject"
    )

    total = sum(result.score for result in results)

    average = round(
        total / results.count(),
        2
    ) if results.exists() else 0

    return render(
        request,
        "examinations/report_card.html",
        {
            "student": student,
            "results": results,
            "total": total,
            "average": average,
        },
    )