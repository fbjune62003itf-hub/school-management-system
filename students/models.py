from django.db import models
from classes.models import SchoolClass


class Student(models.Model):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    gender = models.CharField(max_length=10)

    date_of_birth = models.DateField()

    admission_date = models.DateField()

    admission_number = models.CharField(
        max_length=30,
        unique=True
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    parent_name = models.CharField(max_length=100)

    parent_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"