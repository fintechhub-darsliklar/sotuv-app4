from django.shortcuts import render

# Create your views here.


def monitoring_page(request):
    return render(request, "monitoring.html")


def products_page(request):
    return render(request, "products.html")


def products_create_page(request):
    return render(request, "products-create.html")