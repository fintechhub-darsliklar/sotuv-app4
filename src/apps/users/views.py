from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from apps.order.models import Order, OrderItem
from django.db.models import Sum, F
from datetime import timedelta
from apps.order.models import Order
from apps.product.models import ProductInput

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

    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        days.append(date.strftime('%d-%b'))
        
        day_income = Order.objects.filter(created_at__date=date).aggregate(Sum('total_price'))['total_price__sum'] or 0
        income_list.append(float(day_income))
        
        day_profit = get_actual_profit(date)
        profit_list.append(float(day_profit))

    # ==========================================
    # 3. OXIRGI 5 TA HARAKAT (Kirim va Sotuv)
    # ==========================================
    
    # Har ikkala modeldan oxirgi 5 tasini olamiz (barchasini olmaslik uchun)
    latest_orders = Order.objects.all().order_by('-created_at')[:5]
    latest_inputs = ProductInput.objects.all().order_by('-created_at')[:5]

    activities = []

    # Sotuvlarni ro'yxatga qo'shamiz
    for order in latest_orders:
        activities.append({
            'title': f"Yangi sotuv #{order.id}",
            'desc': 'Kassa 01', # Bu yerni o'zingiz kassir nomiga moslaysiz (masalan: order.cashier.username)
            'time': order.created_at,
            'icon': 'add_shopping_cart',
            'bg_color': 'bg-primary/10',
            'text_color': 'text-primary'
        })

    # Kirimlarni ro'yxatga qo'shamiz
    for p_input in latest_inputs:
        product_name = p_input.product.name if hasattr(p_input, 'product') else "Mahsulot"
        activities.append({
            'title': f"Kirim: {product_name[:15]}...", # Nomi juda uzun bo'lsa kesamiz
            'desc': 'Asosiy ombor',
            'time': p_input.created_at,
            'icon': 'inventory_2',
            'bg_color': 'bg-emerald-500/10',
            'text_color': 'text-emerald-500'
        })

    # Ikkala ro'yxatni vaqti bo'yicha kamayish tartibida saralaymiz (eng yangisi tepada)
    activities.sort(key=lambda x: x['time'], reverse=True)
    
    # Faqat eng oxirgi 5 tasini ajratib olamiz
    recent_activities = activities[:5]


    data = {
        "todays_income": todays_income,
        "todays_profit": todays_profit,
        "labels": days,
        "income_data": income_list,
        "profit_data": profit_list,
        "recent_activities": recent_activities, # Contextga qoshamiz
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