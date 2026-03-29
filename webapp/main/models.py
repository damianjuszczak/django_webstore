from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Kategoria")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, verbose_name="Producent")

    name = models.CharField(max_length=255, verbose_name="Nazwa produktu")
    slug = models.SlugField(unique=True, verbose_name="Slug (URL)")
    description = models.TextField(verbose_name="Opis")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena (PLN)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Ilość w magazynie")

    technical_specs = models.JSONField(default=dict, blank=True, verbose_name="Specyfikacja techniczna")

    is_available = models.BooleanField(default=True, verbose_name="Dostępny")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dodano")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualizacja")

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produkt")
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d', verbose_name="Plik obrazu")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Tekst alternatywny")
    main_photo = models.BooleanField(default=False, verbose_name="Główne zdjęcie?")

    class Meta:
        verbose_name = "Zdjęcie produktu"
        verbose_name_plural = "Galeria zdjęć"

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
        return f"Profil użytkownika: {self.user.username}"