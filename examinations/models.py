from django.db import models
from students.models import Student
from classes.models import SchoolClass


class Examination(models.Model):

    TERM_CHOICES = [
        ("Term 1", "Term 1"),
        ("Term 2", "Term 2"),
        ("Term 3", "Term 3"),
    ]

    SUBJECT_CHOICES = [
    ("English", "English"),
    ("Mathematics", "Mathematics"),
    ("Science", "Science"),
    ("Social Studies", "Social Studies"),
    ("Creative Art", "Creative Art"),
    ("RME", "RME"),
    ("OWOP", "OWOP"),
    ("History", "History"),
    ("French", "French"),
    ("Pre-Tech", "Pre-Tech"),
    ("Home Economics", "Home Economics"),
    ("Fante", "Fante"),
    ("ICT", "ICT"),
]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=50,
        choices=SUBJECT_CHOICES
    )

    term = models.CharField(
        max_length=20,
        choices=TERM_CHOICES
    )

    academic_year = models.CharField(
        max_length=20
    )

    score = models.PositiveIntegerField()

    grade = models.CharField(
        max_length=2,
        blank=True
    )

    remarks = models.CharField(
        max_length=30,
        blank=True
    )

    def save(self, *args, **kwargs):

        if self.score >= 80:
            self.grade = "A"
            self.remarks = "Excellent"

        elif self.score >= 70:
            self.grade = "B"
            self.remarks = "Very Good"

        elif self.score >= 60:
            self.grade = "C"
            self.remarks = "Good"

        elif self.score >= 50:
            self.grade = "D"
            self.remarks = "Pass"

        else:
            self.grade = "F"
            self.remarks = "Fail"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.subject}"