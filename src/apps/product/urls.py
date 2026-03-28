from django.urls import path
from . import views


urlpatterns = [
    path('monitoring/', views.monitoring_page, name="monitoring_page"),
    path('products/', views.products_page, name="products_page"),
    path('products/income/', views.product_income_page, name="product_income_page"),
    path('products/create/', views.products_create_page, name="products_create_page"),
    path('categories/create/', views.categories_create_page, name="categories_create_page"),
    path('categories/delete/<int:pk>', views.category_delete, name="category_delete"),
    path('products/delete/<int:pk>', views.product_delete, name="product_delete"),
    path('products/update/<int:pk>', views.product_update, name="product_update"),
]