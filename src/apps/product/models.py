from django.db import models
from apps.shop.models import Shop

# Create your models here.


class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    products_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    barcode = models.CharField(null=True, blank=True, max_length=50)
    input_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    current_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    qoldiq = models.IntegerField(default=0)
    min_qoldiq = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductInput(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    new_input_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    new_current_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    new_wholesale_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    is_added = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
