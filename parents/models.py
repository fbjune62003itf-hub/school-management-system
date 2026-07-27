from django.db import models


class Parent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    occupation = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"