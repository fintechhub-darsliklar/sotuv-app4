from django.urls import path
from . import views


urlpatterns = [
    path('monitoring/', views.monitoring_page, name="monitoring_page"),
]