from django.shortcuts import render
from django.utils import timezone
from itertools import chain
from apps.product.models import ProductInput
from apps.order.models import Order

def monitoring_page(request):
    # Tab va qidiruv parametrlarini olish (Sukut bo'yicha 'tarix' tabi faol)
    current_tab = request.GET.get('tab', 'tarix') 
    search_query = request.GET.get('q', '')

    # Ma'lumotlarni bazadan tortib olish
    # is_added=True kabi filterlaringiz bo'lsa, shu yerda qoshasiz
    inputs = ProductInput.objects.all() 
    orders = Order.objects.all()

    # Agar qidiruv bo'lsa, nomiga ko'ra filterlash
    if search_query:
        inputs = inputs.filter(product__name__icontains=search_query)
        # Order modelida product maydoni qanday nomlanganiga qarab o'zgartirasiz:
        # orders = orders.filter(product__name__icontains=search_query) 

    transactions = []

    # 1. KIRIM ma'lumotlarini ro'yxatga qo'shish
    if current_tab in ['kirim', 'tarix']:
        for item in inputs:
            transactions.append({
                'id': item.id,
                'type': 'Kirim',
                'product_name': item.product.name if hasattr(item, 'product') else 'Noma\'lum',
                'location': 'Asosiy ombor', # Agar modelingizda ombor maydoni bo'lsa uni yozasiz
                'quantity': item.quantity if hasattr(item, 'quantity') else 0,
                'created_at': item.created_at, # Vaqt maydoni
                'is_positive': True,
                'icon': 'south_east', # Pastga yashil strelka
                'color': 'text-emerald-500',
            })

    # 2. CHIQIM ma'lumotlarini ro'yxatga qo'shish
    if current_tab in ['chiqim', 'tarix']:
        for order in orders:
            transactions.append({
                'id': order.id,
                'type': 'Chiqim',
                # Agar Order ichida product bo'lsa order.product.name yoziladi:
                'product_name': getattr(order, 'product_name', f"Buyurtma #{order.id}"), 
                'location': 'Savdo zali',
                'quantity': order.quantity if hasattr(order, 'quantity') else 1,
                'created_at': order.created_at, # Vaqt maydoni
                'is_positive': False,
                'icon': 'north_east', # Tepaga qizil strelka
                'color': 'text-rose-500',
            })

    # 3. Ikkala ma'lumotni birlashtirib, vaqti bo'yicha kamayish tartibida (yangi eng tepada) saralash
    transactions.sort(key=lambda x: x['created_at'], reverse=True)

    context = {
        'transactions': transactions,
        'current_tab': current_tab,
        'search_query': search_query,
    }
    
    return render(request, "monitoring.html", context)