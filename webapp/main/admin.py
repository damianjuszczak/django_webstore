from django.contrib import admin
from .models import Category, Manufacturer, Product, ProductImage, Order, OrderItem

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(ProductImage)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']