from django.shortcuts import render, get_object_or_404, redirect
from apps.customer.models import Customer
from apps.order.models import Cart
from apps.product.models import Product, Category
# Create your views here.


def sotuv_page(request):
    selected_customer = request.GET.get("customer", None)
    customers = Customer.objects.all()
    cart_list = []
    if selected_customer is None:
        first_customer = customers.first()
        if first_customer:
            selected_customer = first_customer.id
            cart_list = first_customer.carts.all()
            selected_cus = first_customer
        else:
            selected_customer = 0
            selected_cus = None
    else:
        selected_cus = Customer.objects.get(id=selected_customer)
        cart_list = selected_cus.carts.all()
    
    context = {
        "customers": customers,
        "selected_customer": int(selected_customer),
        "cart_list": cart_list,
        "total_price": selected_cus.get_cart_total_price() if selected_cus is not None else 0
    }
    return render(request, 'sotuv.html', context=context)


def sotuv_products_list_page(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    selected_category_id = request.GET.get("category_id", None)
    categories = Category.objects.all()
    if len(categories) == 0:
        selected_category_id = 0
        selected_category = None
    else:
        if selected_category_id is None:
            selected_category = categories.first()
            selected_category_id = categories.first().id
        else:
            selected_category = categories.get(id=selected_category_id)
    products = Product.objects.filter(category=selected_category)
    print("cat id", selected_category_id)
    context = {
        "customer_id": customer_id,
        "categories": categories,
        "products": products,
        "selected_category_id": int(selected_category_id),
        "cart_list_count": customer.carts.count(),
        "total_price": customer.get_cart_total_price()
    }
    return render(request, 'sotuv-products-list.html', context=context)


def cart_add_customer_page(request, customer_id, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product:
        customer = get_object_or_404(Customer, pk=customer_id)
        if customer:
            user = request.user
            cart = Cart.objects.filter(product=product, customer=customer)
            if not cart.exists():
                Cart.objects.create(
                    product=product,
                    customer=customer,
                    quantity=1,
                    staff=user.stuff.first()
                )
            else:
                cart = cart.first()
                cart.quantity += 1
                cart.save()
    return redirect("sotuv_products_list_page", customer_id=customer_id)


def cart_increase_page(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    customer_id = 0
    if cart:
        customer_id = cart.customer.id
        cart.quantity += 1
        cart.save()
    return redirect(f"/sotuv/sotuv-page?customer={customer_id}")


def cart_decrease_page(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    customer_id = 0
    if cart:
        cart.quantity -= 1
        customer_id = cart.customer.id
        if cart.quantity == 0:
            cart.delete()
        else:
            cart.save()
    return redirect(f"/sotuv/sotuv-page?customer={customer_id}")


def cart_clear_page(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if customer:
        customer.carts.all().delete()
    return redirect(f"/sotuv/sotuv-page?customer={pk}")


