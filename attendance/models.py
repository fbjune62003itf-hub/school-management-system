from django.db import models
from students.models import Student
from classes.models import SchoolClass


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Present"
    )

    class Meta:
        unique_together = ("student", "date")

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"