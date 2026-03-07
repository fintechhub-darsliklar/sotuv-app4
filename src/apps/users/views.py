from django.shortcuts import render, redirect

# Create your views here.

def dashboard_page(request):

    if not request.user.is_authenticated:
        return redirect("login_view")

    return render(request, "dashboard.html")


def login_page(request):
    return render(request, "login.html")
