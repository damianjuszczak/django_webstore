from .models import Product, Profile, Category
from .cart import Cart
from .contact import ContactForm

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


def index(request):
    products = Product.objects.filter(is_available=True)
    return render(request, "main/index.html", {"products": products})


def contact(request):
    # Jeśli formularz został wysłany
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            messages.success(
                request, "Dziękujemy za kontakt! Twoja wiadomość została wysłana."
            )
            return redirect("contact")

    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)

    messages.success(request, f'Produkt "{product.name}" został dodany do koszyka!')

    previous_url = request.META.get("HTTP_REFERER")

    if previous_url:
        return redirect(previous_url)
    else:
        return redirect("home")


def cart_decrement(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrement(product)

    if str(product_id) not in request.session.get("cart", {}):
        messages.info(request, f'Produkt "{product.name}" został usunięty z koszyka.')

    return redirect("cart")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    messages.info(request, f'Produkt "{product.name}" został usunięty z koszyka.')

    return redirect("cart")


def cart(request):
    cart = Cart(request)
    return render(request, "main/cart.html", {"cart": cart})


def about(request):
    return render(request, "main/about.html")


def search(request):
    query = request.GET.get("q", "")
    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(manufacturer__name__icontains=query)
            | Q(description__icontains=query),
            is_available=True,
        )

    return render(request, "main/search.html", {"products": products, "query": query})


def category_details(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category, is_available=True)

    return render(
        request, "main/category.html", {"category": category, "products": products}
    )


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)

    return render(request, "main/product_details.html", {"product": product})


@login_required
def profile_view(request):
    return render(request, "main/account/profile.html", {"user": request.user})


# Using the Django authentication system (Django Documentation)
# https://docs.djangoproject.com/en/5.1/topics/auth/default/
def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(
                request, f"Pomyślnie zalogowano. Cieszymy się, że z nami jesteś!"
            )

            if request.session.get("next"):
                return redirect(request.session.pop("next"))

            return redirect("home")
        else:
            messages.error(request, "Nieprawidłowy login lub hasło.")
            return redirect("login_user")

    if request.GET.get("next"):
        request.session["next"] = request.GET["next"]

    return render(request, "main/account/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        profile, created = Profile.objects.get_or_create(user=user)

        profile.phone = request.POST.get("phone", "")
        profile.address = request.POST.get("adress", "")
        profile.city = request.POST.get("city", "")
        profile.zip_code = request.POST.get("zip_code", "")
        profile.country = request.POST.get("country", "Polska")

        profile.save()

        messages.success(request, "Twoje konto zostało pomyślnie utworzone.")
        login(request, user)
        return redirect("home")

    return render(request, "main/account/register.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Pomyślnie wylogowano. Zapraszamy ponownie!")
    return redirect("home")


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Twoje konto zostało pomyślnie usunięte.")
        return redirect("home")

    return redirect("profile")
