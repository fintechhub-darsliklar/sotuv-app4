from django.shortcuts import render, redirect
from .models import Customer
# Create your views here.


def customer_create(request):
    active_last_customer = Customer.objects.filter(is_active=True).last()
    if active_last_customer is None:
        number = 1
    else:
        number = active_last_customer.order_number + 1
    customer = Customer.objects.create(
        order_number=number
    )
    return redirect(f"/sotuv/sotuv-page?customer={customer.id}")


def customer_delete(request, pk):
    print("ochirish page", pk)
    active_customers = Customer.objects.filter(is_active=True)
    command_update = False
    for customers in active_customers:
        if command_update:
            customers.order_number -= 1
            customers.save()
        if customers.id == pk:
            customers.delete()
            command_update = True

    return redirect("sotuv_page")
