from django.db import models
from teachers.models import Teacher


class Subject(models.Model):

    subject_name = models.CharField(
        max_length=100,
        unique=True
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_subjects"
    )

    class Meta:
        ordering = [
            "subject_name"
        ]

    def __str__(self):
        return self.subject_name