from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Fee
from .forms import FeeForm
from classes.models import SchoolClass
from accounts.decorators import admin_required


@admin_required
def fee_list(request):

    classes = SchoolClass.objects.all().order_by("class_name")

    fees = Fee.objects.select_related(
        "student",
        "school_class"
    ).order_by(
        "-payment_date",
        "student__first_name"
    )

    class_id = request.GET.get("class", "").strip()
    term = request.GET.get("term", "").strip()
    year = request.GET.get("year", "").strip()
    search = request.GET.get("search", "").strip()

    if class_id:
        fees = fees.filter(school_class_id=class_id)

    if term:
        fees = fees.filter(term__icontains=term)

    if year:
        fees = fees.filter(academic_year__icontains=year)

    if search:
        fees = fees.filter(
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(student__admission_number__icontains=search)
        )

    return render(
        request,
        "fees/fee_list.html",
        {
            "fees": fees,
            "classes": classes,
            "selected_class": class_id,
            "selected_term": term,
            "selected_year": year,
            "search": search,
        },
    )


@admin_required
def add_fee(request):

    if request.method == "POST":

        form = FeeForm(request.POST)

        if form.is_valid():

            fee = form.save(commit=False)

            if fee.amount_paid <= 0:
                fee.status = "Unpaid"

            elif fee.amount_paid < fee.amount:
                fee.status = "Partial"

            else:
                fee.status = "Paid"

            fee.save()

            return redirect("fee-list")

    else:

        form = FeeForm()

    return render(
        request,
        "fees/add_fee.html",
        {
            "form": form
        }
    )


@admin_required
def edit_fee(request, id):

    fee = get_object_or_404(Fee, id=id)

    if request.method == "POST":

        form = FeeForm(request.POST, instance=fee)

        if form.is_valid():

            fee = form.save(commit=False)

            if fee.amount_paid <= 0:
                fee.status = "Unpaid"

            elif fee.amount_paid < fee.amount:
                fee.status = "Partial"

            else:
                fee.status = "Paid"

            fee.save()

            return redirect("fee-list")

    else:

        form = FeeForm(instance=fee)

    return render(
        request,
        "fees/edit_fee.html",
        {
            "form": form
        }
    )


@admin_required
def delete_fee(request, id):

    fee = get_object_or_404(Fee, id=id)

    if request.method == "POST":
        fee.delete()
        return redirect("fee-list")

    return render(
        request,
        "fees/delete_fee.html",
        {
            "fee": fee
        }
    )