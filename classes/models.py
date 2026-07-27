from django.db import models


class SchoolClass(models.Model):
    class_name = models.CharField(max_length=100)
    class_teacher = models.CharField(
    max_length=100,
    blank=True,
    default=""
)
    capacity = models.PositiveIntegerField(default=40)

    def __str__(self):
        return self.class_name