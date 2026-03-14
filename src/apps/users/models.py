from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return f"{self.phone_number}, {self.get_full_name()}"


class StaffRole(models.TextChoices):
    SELLER = ("SELLER", "seller")
    ADMIN = ("ADMIN", "admin")
    MANAGER = ("MANAGER", "manager")


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="stuff")
    shop = models.ForeignKey(
        "shop.Shop", on_delete=models.SET_NULL, null=True, blank=True
    )
    role = models.CharField(max_length=50, choices=StaffRole.choices)
    avatar = models.ImageField(null=True, blank=True, upload_to="staff_avatar/")
    todays_income = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.get_full_name()} | {self.role}"
