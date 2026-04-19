from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa kategorii")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug (URL)")

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'category_slug': self.slug})

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Producent")
    website = models.URLField(blank=True, verbose_name="Strona WWW")

    class Meta:
        verbose_name = "Producent"
        verbose_name_plural = "Producenci"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    technical_specs = models.JSONField(default=dict, blank=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d')
    alt_text = models.CharField(max_length=200, blank=True)
    main_photo = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, blank=True)

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, default="Polska")

    newsletter = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Profil: {self.user.username}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nowe'),
        ('processing', 'W trakcie realizacji'),
        ('shipped', 'Wysłane'),
        ('completed', 'Zrealizowane'),
        ('cancelled', 'Anulowane'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default="Polska")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Zamówienie #{self.id} - {self.user.username}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Pozycja zamówienia"
        verbose_name_plural = "Pozycje zamówienia"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)