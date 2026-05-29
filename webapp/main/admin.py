from django.contrib import admin
from .models import Category, Manufacturer, Product, ProductImage, Order, OrderItem,ContactMessage, WishlistItem

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(WishlistItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'status', 'created_at']
    list_filter = ['paid', 'status', 'created_at', 'delivery_method']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'stripe_id']
    inlines = [OrderItemInline]
    actions = ['mark_as_processing']

    @admin.action(description="Zmień status zaznaczonych na 'W trakcie realizacji'")
    def mark_as_processing(self, request, queryset):
        updated = queryset.filter(paid=True).update(status='processing')
        self.message_user(request, f"Zaktualizowano {updated} zamówień do statusu 'W trakcie realizacji'.")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'created_at')