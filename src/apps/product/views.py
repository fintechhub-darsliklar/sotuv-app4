from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, ProductInput
from django.db.models import Sum, F
from decimal import Decimal, InvalidOperation
# Create your views here.



def products_page(request):
    category_id = request.GET.get("category_id", 'all')
    if category_id == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__id=category_id)
        category_id = int(category_id)
    categories = Category.objects.all()
    context = {
        'products': products,
        "categories": categories,
        "selected_category_id": category_id
    }
    return render(request, "products.html", context=context)


def products_create_page(request):
    if request.method == 'POST':
        image_file = request.FILES.get("image") 
        data = request.POST            
        product_name = data.get("product_name")
        product_barcode = data.get("product_barcode")
        product_category = data.get("product_category")
        input_price = data.get("input_price")
        current_price = data.get("current_price")
        wholesale_price = data.get("wholesale_price")
        qoldiq = data.get("qoldiq")
        min_qoldiq = data.get("min_qoldiq")
        status = data.get("status")
        try:
            category = Category.objects.get(id=product_category)
            product = Product.objects.create(
                category = category, 
                name = product_name,
                image = image_file,
                barcode = product_barcode,
                input_price = input_price,
                current_price = current_price,
                wholesale_price = wholesale_price,
                qoldiq = qoldiq,
                min_qoldiq = min_qoldiq,
                is_active = True if status == "on" else False
            )
        except Category.DoesNotExist:
            msg = "Category yoq yoki tanlanmadi!"
        return redirect("products_page")
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, "products-create.html", context=context)


def categories_create_page(request):
    if request.method == 'POST':
        data = request.POST  
        category_name = data.get("category_name")
        shop = request.user.stuff.first().shop
        if category_name and shop:
            Category.objects.create(
                name=category_name,
                shop=shop
            )
        return redirect("products_page")
    return render(request, "category-create.html", context={})


def category_delete(request, pk):
    Category.objects.get(id=pk).delete()
    return redirect("products_page")


def product_delete(request, pk):
    Product.objects.get(id=pk).delete()
    return redirect("products_page")


def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        product.name = request.POST.get("product_name")
        product.barcode = request.POST.get("product_barcode")
        product.input_price = request.POST.get("input_price")
        product.current_price = request.POST.get("current_price")
        product.wholesale_price = request.POST.get("wholesale_price")
        product.qoldiq = request.POST.get("qoldiq")
        product.min_qoldiq = request.POST.get("min_qoldiq")
        product.status = True if request.POST.get("status") else False

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        return redirect("products_page")

    return render(request, "products-update.html", {
        "product": product,
        "categories": Category.objects.all()
    })


def product_income_page(request):

    if request.method == "POST":
        product_incomes_data = ProductInput.objects.filter(is_added=False)
        for pi in product_incomes_data:
            try:
                # Formadan kelgan ma'lumotdan vergul va bo'shliqlarni olib tashlaymiz
                i_price = request.POST.get(f"input_price_{pi.product.id}", 0)
                w_price = request.POST.get(f"wholesale_price_{pi.product.id}", 0)
                c_price = request.POST.get(f"current_price_{pi.product.id}", 0)
                pi.product.qoldiq += pi.quantity
                pi.product.current_price = Decimal(c_price) if c_price else Decimal('0.00')
                pi.product.input_price = Decimal(i_price) if i_price else Decimal('0.00')
                pi.product.wholesale_price = Decimal(w_price) if w_price else Decimal('0.00')
                pi.is_added = True
                pi.product.save()
                pi.save()
            except (InvalidOperation, IndexError) as e:
                # Agar noto'g'ri raqam kiritilsa yoki index topilmasa nima qilish kerakligini shu yerda yozasiz
                print(f"Xatolik yuz berdi: {e}")
        return redirect("dashboard_page")

    action = request.GET.get("action", 'list')
    if action == "delete":
        p_i_id = request.GET.get("p_i_id", None)
        if p_i_id:
            pi = ProductInput.objects.filter(id=p_i_id)
            pi.delete()
    elif action == "decrease":
        p_i_id = request.GET.get("p_i_id", None)
        if p_i_id:
            pi = ProductInput.objects.get(id=p_i_id)
            pi.quantity -= 1
            if pi.quantity == 0:
                pi.delete()
            else:
                pi.save()
    elif action == "increase":
        p_i_id = request.GET.get("p_i_id", None)
        if p_i_id:
            pi = ProductInput.objects.get(id=p_i_id)
            pi.quantity += 1
            pi.save()

    product_incomes_data = ProductInput.objects.filter(is_added=False)
    total_input_price = product_incomes_data.aggregate(
        total=Sum(F('quantity') * F('product__input_price'))
    )['total'] or 0
    
    context = {
        "product_incomes_data": product_incomes_data,
        "total_input_price": total_input_price
    }
    return render(request, "products-income.html", context=context)



def product_income_products_page(request):
    category_id = request.GET.get("category_id", 'all')
    product_id = request.GET.get("product_id", None)
    barcode = request.GET.get("barcode", None)

    if product_id or barcode:
        print("barcode", barcode)
        if product_id:
            product = Product.objects.filter(id=product_id)
        else:
            product = Product.objects.filter(barcode=barcode)
            print(product)
        if product.exists():
            product = product.first()
            product_income = ProductInput.objects.filter(product=product, is_added=False)
            if product_income.exists():
                pi = product_income.first()
                pi.quantity += 1
                pi.save()
            else:
                ProductInput.objects.create(
                    product=product,
                    quantity=1,
                    new_input_price=product.input_price,
                    new_current_price=product.current_price,
                    new_wholesale_price=product.wholesale_price,
                )
        return redirect('product_income_page')
    
    
    if category_id == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__id=category_id)
        category_id = int(category_id)
    categories = Category.objects.all()
    context = {
        'products': products,
        "categories": categories,
        "selected_category_id": category_id
    }
    return render(request, "product-income-products.html", context=context)

