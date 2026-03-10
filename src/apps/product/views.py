from django.shortcuts import render

# Create your views here.


def monitoring_page(request):
    return render(request, "monitoring.html")
