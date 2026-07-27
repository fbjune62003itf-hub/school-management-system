from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from students.models import Student
from teachers.models import Teacher
from parents.models import Parent
from classes.models import SchoolClass
from attendance.models import Attendance
from fees.models import Fee
from examinations.models import Examination
from subjects.models import Subject


def report_dashboard(request):

    context = {
        "students": Student.objects.count(),
        "teachers": Teacher.objects.count(),
        "parents": Parent.objects.count(),
        "classes": SchoolClass.objects.count(),
        "subjects": Subject.objects.count(),
        "attendance": Attendance.objects.count(),
        "fees": Fee.objects.count(),
        "examinations": Examination.objects.count(),
    }

    return render(
        request,
        "reports/report_dashboard.html",
        context,
    )


def student_report(request):

    students = Student.objects.select_related(
        "school_class"
    ).order_by(
        "first_name"
    )

    classes = SchoolClass.objects.all().order_by(
        "class_name"
    )

    admission_from = request.GET.get(
        "admission_from",
        ""
    )

    admission_to = request.GET.get(
        "admission_to",
        ""
    )

    selected_class = request.GET.get(
        "class",
        ""
    )

    if admission_from:
        students = students.filter(
            admission_date__gte=admission_from
        )

    if admission_to:
        students = students.filter(
            admission_date__lte=admission_to
        )

    if selected_class:
        students = students.filter(
            school_class_id=selected_class
        )

    return render(
        request,
        "reports/student_report.html",
        {
            "students": students,
            "classes": classes,
            "admission_from": admission_from,
            "admission_to": admission_to,
            "selected_class": selected_class,
        },
    )


def teacher_report(request):

    teachers = Teacher.objects.all().order_by(
        "first_name"
    )

    return render(
        request,
        "reports/teacher_report.html",
        {
            "teachers": teachers,
        },
    )


def fee_report(request):

    fees = Fee.objects.all().order_by("-id")

    return render(
        request,
        "reports/fee_report.html",
        {
            "fees": fees,
        },
    )


def attendance_report(request):

    attendance = Attendance.objects.select_related(
        "student"
    ).order_by("-date")

    return render(
        request,
        "reports/attendance_report.html",
        {
            "attendance": attendance,
        },
    )


def examination_report(request):

    classes = SchoolClass.objects.all().order_by(
        "class_name"
    )

    students = Student.objects.all().order_by(
        "first_name",
        "last_name"
    )

    years = (
        Examination.objects
        .values_list(
            "academic_year",
            flat=True
        )
        .distinct()
        .order_by(
            "academic_year"
        )
    )

    terms = [
        "Term 1",
        "Term 2",
        "Term 3",
    ]

    selected_class = request.GET.get(
        "class",
        ""
    )

    selected_student = request.GET.get(
        "student",
        ""
    )

    selected_year = request.GET.get(
        "year",
        ""
    )

    selected_term = request.GET.get(
        "term",
        ""
    )

    examinations = Examination.objects.select_related(
        "student",
        "school_class",
    ).order_by("subject")

    if selected_class:
        examinations = examinations.filter(
            school_class_id=selected_class
        )

    if selected_student:
        examinations = examinations.filter(
            student_id=selected_student
        )

    if selected_year:
        examinations = examinations.filter(
            academic_year=selected_year
        )

    if selected_term:
        examinations = examinations.filter(
            term=selected_term
        )

    student = None

    if selected_student:
        student = Student.objects.filter(
            id=selected_student
        ).first()

    total_score = (
        examinations.aggregate(
            total=Sum("score")
        )["total"] or 0
    )

    subject_count = examinations.count()

    average = round(
        total_score / subject_count,
        2
    ) if subject_count else 0

    if average >= 80:
        overall = "Excellent"

    elif average >= 70:
        overall = "Very Good"

    elif average >= 60:
        overall = "Good"

    elif average >= 50:
        overall = "Pass"

    else:
        overall = "Fail"

    return render(
        request,
        "reports/examination_report.html",
        {
            "classes": classes,
            "students": students,
            "years": years,
            "terms": terms,
            "selected_class": selected_class,
            "selected_student": selected_student,
            "selected_year": selected_year,
            "selected_term": selected_term,
            "student": student,
            "examinations": examinations,
            "total_score": total_score,
            "average": average,
            "overall": overall,
        },
    )


def export_exam_pdf(request):

    selected_student = request.GET.get(
        "student",
        ""
    )

    selected_year = request.GET.get(
        "year",
        ""
    )

    selected_term = request.GET.get(
        "term",
        ""
    )

    examinations = Examination.objects.select_related(
        "student"
    )

    if selected_student:
        examinations = examinations.filter(
            student_id=selected_student
        )

    if selected_year:
        examinations = examinations.filter(
            academic_year=selected_year
        )

    if selected_term:
        examinations = examinations.filter(
            term=selected_term
        )

    student = None

    if selected_student:
        student = Student.objects.get(
            id=selected_student
        )

    total_score = (
        examinations.aggregate(
            total=Sum("score")
        )["total"] or 0
    )

    count = examinations.count()

    average = round(
        total_score / count,
        2
    ) if count else 0

    if average >= 80:
        overall = "Excellent"

    elif average >= 70:
        overall = "Very Good"

    elif average >= 60:
        overall = "Good"

    elif average >= 50:
        overall = "Pass"

    else:
        overall = "Fail"

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'filename="Examination_Report.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b><font size=18>FRANCO SCHOOL MANAGEMENT SYSTEM</font></b>",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            "STUDENT EXAMINATION REPORT",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 20))

    if student:

        story.append(
            Paragraph(
                f"<b>Student:</b> {student.first_name} {student.last_name}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Admission Number:</b> {student.admission_number}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Class:</b> {student.school_class}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Academic Year:</b> {selected_year}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Term:</b> {selected_term}",
                styles["Normal"],
            )
        )

        story.append(Spacer(1, 20))

    data = [

        [
            "Subject",
            "Score",
            "Grade",
            "Remarks",
        ]

    ]

    for exam in examinations:

        data.append(

            [
                exam.subject,
                str(exam.score),
                exam.grade,
                exam.remarks,
            ]

        )

    table = Table(data)

    table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.darkgreen,
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.beige,
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    10,
                ),

            ]

        )

    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(

        Paragraph(
            f"<b>Total Score:</b> {total_score}",
            styles["Normal"],
        )

    )

    story.append(

        Paragraph(
            f"<b>Average Score:</b> {average}",
            styles["Normal"],
        )

    )

    story.append(

        Paragraph(
            f"<b>Overall Performance:</b> {overall}",
            styles["Normal"],
        )

    )

    story.append(Spacer(1, 20))

    story.append(

        Paragraph(
            "Generated by Franco School Management System",
            styles["Italic"],
        )

    )

    doc.build(story)

    return response