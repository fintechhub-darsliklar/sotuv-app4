from django.db import models

# Create your models here.


class PaymentType(models.TextChoices):
    CASH = ("CASH", "cash")
    CART = ("CART", "cart")


class Order(models.Model):
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE)
    staff = models.ForeignKey("users.Staff", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    payment_type = models.CharField(max_length=10, choices=PaymentType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer} | {self.total_price}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    staff = models.ForeignKey("users.Staff", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE, related_name="carts")
    staff = models.ForeignKey("users.Staff", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
