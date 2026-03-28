from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Order, OrderItem, Cart

# --- Resources (Import/Export uchun maydonlarni belgilash) ---

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        # Qaysi maydonlar eksport/import bo'lishini tanlash mumkin
        fields = ('id', 'customer__order_number', 'staff__user__username', 'total_price', 'payment_type', 'created_at')

class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem

class CartResource(resources.ModelResource):
    class Meta:
        model = Cart

# --- Admin Classes ---

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('id', 'customer', 'staff', 'total_price', 'payment_type', 'created_at')
    list_filter = ('payment_type', 'created_at', 'staff')
    search_fields = ('staff__username',)
    date_hierarchy = 'created_at' # Vaqt bo'yicha navigatsiya
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(ImportExportModelAdmin):
    resource_class = OrderItemResource
    list_display = ('id', 'order', 'product', 'quantity', 'total_price', 'staff')
    list_filter = ('product', 'staff')
    search_fields = ('order__id', 'product__name')

@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    resource_class = CartResource
    list_display = ('id', 'customer', 'product', 'quantity', 'staff', 'updated_at')
    list_filter = ('customer', 'staff')
    search_fields = ( 'product__name',)