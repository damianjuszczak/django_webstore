from django.contrib import admin
from .models import Category, Manufacturer, Product, ProductImage

# To sprawi, że zdjęcia będą widoczne wewnątrz edycji produktu
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Ile pustych pól na zdjęcia ma się wyświetlać domyślnie

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'price', 'stock', 'is_available']
    prepopulated_fields = {'slug': ('name',)} # Automatycznie wpisze slug, gdy będziesz pisać nazwę!
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Manufacturer)