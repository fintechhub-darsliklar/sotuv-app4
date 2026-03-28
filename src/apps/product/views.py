from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, ProductInput
# Create your views here.


def monitoring_page(request):
    return render(request, "monitoring.html")


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

    product_incomes_data = ProductInput.objects.filter(is_added=False)
    context = {
        "product_incomes_data": product_incomes_data
    }
    print(product_incomes_data)
    return render(request, "products-income.html", context=context)