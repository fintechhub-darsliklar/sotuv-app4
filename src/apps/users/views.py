from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from apps.order.models import Order, OrderItem
from django.db.models import Sum, F
from datetime import timedelta

# Create your views here.


def get_actual_profit(today):
    # OrderItem orqali har bir mahsulotning (Sotilgan narxi - Tannarxi) * Soni ni hisoblaymiz
    profit = OrderItem.objects.filter(created_at__date=today).aggregate(
        total_profit=Sum(
            (F('total_price') - (F('product__input_price') * F('quantity')))
        )
    )
    return profit['total_profit'] or 0


def dashboard_page(request):
    if not request.user.is_authenticated:
        return redirect("login_page")

    today = timezone.now().date()
    
    # 1. Bugungi qisqa statistika
    todays_result = Order.objects.filter(created_at__date=today).aggregate(Sum('total_price'))
    todays_income = todays_result['total_price__sum'] or 0
    todays_profit = get_actual_profit(today)

    # 2. 1 haftalik diagramma uchun ma'lumotlar
    days = []
    income_list = []
    profit_list = []

    # Oxirgi 7 kunni siklda aylanamiz (bugun bilan birga)
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        days.append(date.strftime('%d-%b')) # Masalan: '28-Mar'
        
        # Shu kundagi savdo (Income)
        day_income = Order.objects.filter(created_at__date=date).aggregate(Sum('total_price'))['total_price__sum'] or 0
        income_list.append(float(day_income))
        
        # Shu kundagi foyda (Profit)
        day_profit = get_actual_profit(date)
        profit_list.append(float(day_profit))

    data = {
        "todays_income": todays_income,
        "todays_profit": todays_profit,
        # Diagramma uchun kerakli listlar
        "labels": days,
        "income_data": income_list,
        "profit_data": profit_list,
    }

    return render(request, "dashboard.html", context=data)

def login_page(request):
    msg = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard_page")
        msg = "login yoki parol xato!"
    
    context = {"msg": msg}
    return render(request, "login.html", context=context)


def logout_page(request):
    logout(request)
    return redirect("login_page")