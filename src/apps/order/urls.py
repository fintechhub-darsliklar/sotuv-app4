from django.urls import path
from . import views


urlpatterns = [
    path('sotuv-page/', views.sotuv_page, name="sotuv_page"),
    path('sotuv/products/customer/<int:customer_id>', views.sotuv_products_list_page, name="sotuv_products_list_page"),
    path('cart/add/customer-with/<int:customer_id>/<int:product_id>', views.cart_add_customer_page, name="cart_add_customer_page"),
    path('cart/update/increase/<int:pk>/', views.cart_increase_page, name="cart_increase_page"),
    path('cart/update/decrease/<int:pk>/', views.cart_decrease_page, name="cart_decrease_page"),
    path('cart/delete/customer-with/<int:pk>/', views.cart_clear_page, name="cart_clear_page"),
]