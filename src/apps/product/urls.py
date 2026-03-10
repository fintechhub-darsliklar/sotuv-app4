from django.urls import path
from . import views


urlpatterns = [
    path('monitoring/', views.monitoring_page, name="monitoring_page"),
    path('products/', views.products_page, name="products_page"),
    path('products/create/', views.products_create_page, name="products_create_page"),
]