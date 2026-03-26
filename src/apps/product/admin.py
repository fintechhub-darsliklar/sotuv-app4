from django.contrib import admin
from .models import Category, Product, ProductInput
from .resources import ProductResource, CategoryResource
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(ProductInput)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ("name", "barcode", "qoldiq", "is_active")
    resource_classes = (ProductResource,)
    list_filter = ("is_active", "created_at", "category")
    search_fields = ("name", )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    resource_classes = (CategoryResource,)


