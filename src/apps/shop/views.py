from django.shortcuts import render, redirect
from django.utils import timezone
from apps.order.models import Order
from django.db.models import Sum
from apps.shop.models import Shop
from apps.users.models import Staff, StaffRole,User

# Create your views here.

def profile_page(request):
    
    return render(request, "profile.html")


def xodimlar_page(request):
    if request.user.stuff.last().role == "SELLER":
        return redirect("dashboard_page")
    today = timezone.now().date()
    # 1. Bugungi qisqa statistika
    todays_result = Order.objects.filter(created_at__date=today).aggregate(Sum('total_price'))
    todays_income = todays_result['total_price__sum'] or 0
    shop = request.user.stuff.last().shop
    stuff_list = Staff.objects.filter(shop=shop)
    top_staff = stuff_list.order_by('-todays_income').first()
    
    context = {
        "todays_income": todays_income,
        "stuff_list": stuff_list,
        "top_staff": top_staff,

    }
    return render(request, "xodimlar.html", context=context)


def xodim_qoshish_page(request):
    if request.user.stuff.last().role == "SELLER":
        return redirect("dashboard_page")
    if request.POST:
        data = request.POST
        shop = request.user.stuff.last().shop
        user = User.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("phone_number"),
            password=data.get("password")
        )
        user.set_password(data.get("password"))
        user.save()
        Staff.objects.create(
            user=user,
            shop=shop
        )
        return redirect("xodimlar_page")
    return render(request, "xodim-qoshish.html")


def xodim_taxrirlash_page(request, xodim_id):
    if request.user.stuff.last().role == "SELLER":
        return redirect("dashboard_page")
    xodim = Staff.objects.get(id=xodim_id)
    
    if request.POST:
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        role = data.get("role")
        password = data.get("password")
        xodim.user.first_name = first_name
        xodim.user.last_name = last_name
        xodim.user.username = username
        if password:
            xodim.user.set_password(password)
        xodim.user.save()
        xodim.role = role
        xodim.save()
        if request.user == xodim.user and password:
            return redirect("login_page")
        return redirect("xodimlar_page")
    
    roles = [
    {
        "name": "ADMIN",
        "display": "Admin"
    },
    {
        "name": "SELLER",
        "display": "Sotuvchi"
    },
    {
        "name": "MANAGER",
        "display": "Manager"
    },
    ]
    context = {
        "xodim": xodim,
        "roles": roles
    }
    return render(request, "xodim-taxrirlash.html", context=context)


def xodim_delete_page(request, xodim_id):
    if request.user.stuff.last().role == "SELLER":
        return redirect("dashboard_page")
    xodim = Staff.objects.get(id=xodim_id)
    user = xodim.user
    xodim.delete()
    user.delete()
    return redirect("xodimlar_page")

