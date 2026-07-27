from django.db import models
from classes.models import SchoolClass
from students.models import Student


class Fee(models.Model):

    STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Partial", "Partial"),
        ("Unpaid", "Unpaid"),
    ]

    
    school_class = models.ForeignKey(
    SchoolClass,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_date = models.DateField()

    term = models.CharField(
        max_length=30
    )

    academic_year = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Unpaid"
    )

@property
def balance(self):
    return self.amount - self.amount_paid

def __str__(self):
        return f"{self.student} - {self.term} ({self.academic_year})"