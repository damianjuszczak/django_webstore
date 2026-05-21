from .models import Product, Profile, Category, Order, OrderItem, ContactMessage, WishlistItem
from .cart import Cart
from .contact import ContactForm

from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.db import transaction, IntegrityError
from django.views.decorators.http import require_POST
from django.conf import settings
from main.utilities import get_live_exchange_rates


def index(request):
    products = (
        Product.objects.select_related("manufacturer")
        .prefetch_related("images")
        .filter(is_available=True)
        .order_by("?")[:4]
    )
    return render(request, "main/index.html", {"products": products})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            ContactMessage.objects.create(
                email=form.cleaned_data["email"],
                title=form.cleaned_data["title"],
                message=form.cleaned_data["message"],
            )
            messages.success(
                request, "Dziękujemy za kontakt! Twoja wiadomość została zapisana."
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

    products = (
        Product.objects.select_related("manufacturer")
        .prefetch_related("images")
        .filter(category=category, is_available=True)
    )

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    currency = request.session.get(
        "currency", getattr(settings, "DEFAULT_CURRENCY", "PLN")
    )
    live_rates = get_live_exchange_rates()
    rate = live_rates.get(currency, 1.0)
    ram = request.GET.get("ram")
    cpu = request.GET.get("cpu")

    try:
        if min_price:
            # convert user curreny choice to the one in database
            converted_min = float(min_price) / float(rate)
            products = products.filter(price__gte=converted_min)
        if max_price:
            # convert user curreny choice to the one in database
            converted_max = float(max_price) / float(rate)
            products = products.filter(price__lte=converted_max)
    except ValueError:
        pass

    if ram:
        products = products.filter(ram__icontains=ram)

    if cpu:
        products = products.filter(cpu__icontains=cpu)

    context = {
        "category": category,
        "products": products,
        "min_price": min_price,
        "max_price": max_price,
        "ram": ram,
        "cpu": cpu,
    }

    return render(request, "main/category.html", context)


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, "main/product_details.html", {"product": product})


def change_currency(request):
    if request.method == "POST":
        currency = request.POST.get("currency", "PLN")

        allowed_currencies = ["PLN", "EUR", "USD"]

        if currency in allowed_currencies:
            request.session["currency"] = currency  # save to user session

    next_url = request.POST.get("next", "/")  # redirect back to the same page
    return redirect(next_url)


def login_form(request):
    return render(request, "main/account/login.html")


def register_form(request):
    return render(request, "main/account/register.html")


@require_POST
def auth_login(request):
    if request.user.is_authenticated:
        messages.success(request, "Już jesteś zalogowany.")
        return JsonResponse({"status": "success", "redirect_url": "/"})

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "Pomyślnie zalogowano.")
        return JsonResponse({"status": "success", "redirect_url": "/profile/"})
    else:
        return JsonResponse(
            {"status": "error", "message": "Błędne dane logowania"}, status=401
        )


@require_POST
def auth_register(request):
    if request.user.is_authenticated:
        messages.error(
            request, "Wyloguj się i spróbuje ponownie zarejestrować nowe konto."
        )
        return JsonResponse({"status": "success", "redirect_url": "/"})

    try:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        profile, created = Profile.objects.get_or_create(user=user)

        profile.phone = request.POST.get("phone", "")
        profile.address = request.POST.get("address", "")
        profile.city = request.POST.get("city", "")
        profile.zip_code = request.POST.get("zip_code", "")
        profile.country = request.POST.get("country", "Polska")

        profile.save()

        login(request, user)
        messages.success(request, "Twoje konto zostało pomyślnie utworzone.")
        return JsonResponse({"status": "success", "redirect_url": "/profile/"})
    except IntegrityError:
        return JsonResponse(
            {"status": "error", "message": "Ten login jest już zajęty."}, status=400
        )
    except Exception:
        return JsonResponse(
            {"status": "error", "message": "Coś poszło nie tak podczas rejestracji."},
            status=500,
        )


@require_POST
def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Pomyślnie wylogowano.")
        return JsonResponse({"status": "success", "redirect_url": "/"})
    return JsonResponse({"status": "success", "redirect_url": "/"})


@login_required
@require_POST
def profile_change_info(request):
    try:
        data = request.POST
        user = request.user

        with transaction.atomic():
            user.profile.phone = data.get("phone", user.profile.phone)
            user.email = data.get("email", user.email)
            user.profile.address = data.get("address", user.profile.address)
            user.profile.zip_code = data.get("zip_code", user.profile.zip_code)
            user.profile.city = data.get("city", user.profile.city)
            user.profile.save()
            user.save()
        return JsonResponse(
            {"status": "success", "message": "Dane zostały zaktualizowane."}
        )

    except Profile.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Profil nie istnieje."}, status=404
        )
    except Exception as e:
        messages.error(request, "Coś poszło nie tak, spróbuj ponownie.")
        import traceback

        print(traceback.format_exc())
        return JsonResponse(
            {"status": "error", "redirect_url": "/profile/"}, status=500
        )


@login_required
def profile_info(request):
    return render(
        request,
        "main/account/profile_info.html",
        {"user": request.user, "active_tab": "info"},
    )


@login_required
def profile_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(
        request,
        "main/account/profile_orders.html",
        {"user": request.user, "orders": orders, "active_tab": "orders"},
    )


@login_required
def profile_reports(request):
    return render(
        request,
        "main/account/profile_reports.html",
        {"user": request.user, "active_tab": "reports"},
    )


@login_required
@require_POST
def profile_delete(request):
    try:
        user = request.user
        user.delete()
        return JsonResponse({"status": "success", "redirect_url": "/"}, status=200)

    except Exception:
        messages.error(
            request, "Wystąpił nieoczekiwany błąd. Nie udało się usunąć konta."
        )
        return JsonResponse(
            {"status": "error", "message": "Nie udało się usunąc konta."}, status=500
        )


def process_order_items(order, items_list, request):
    items_added = 0
    for item in items_list:
        product = item["product"]
        quantity = item["quantity"]

        updated = Product.objects.filter(id=product.id, stock__gte=quantity).update(
            stock=F("stock") - quantity
        )

        if updated:
            OrderItem.objects.create(
                order=order, product=product, price=product.price, quantity=quantity
            )
            items_added += 1
        else:
            messages.warning(request, f"Produkt {product.name} jest niedostępny.")
    return items_added


@login_required
@transaction.atomic
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Twój koszyk jest pusty.")
        return redirect("cart_view")

    order = Order.objects.create(
        user=request.user,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        email=request.user.email,
        phone=request.user.profile.phone,
        address=request.user.profile.address,
        city=request.user.profile.city,
        zip_code=request.user.profile.zip_code,
        country=request.user.profile.country,
    )

    items_to_add = [
        {"product": item["product"], "quantity": item["quantity"]} for item in cart
    ]
    added_count = process_order_items(order, items_to_add, request)

    referer_url = request.META.get("HTTP_REFERER", "")
    if added_count > 0:
        request.session["cart"] = {}
        request.session.modified = True

        if "/profile/orders" in referer_url:
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Zamówienie zostało złożone.",
                },
                status=200,
            )

        else:
            messages.success(request, "Zamówienie zostało złożone.")
            return redirect("profile_orders")

    else:
        transaction.set_rollback(True)
        if "/profile/orders" in referer_url:
            return JsonResponse(
                {"status": "error", "message": "Brak produktów na stanie."}, status=400
            )
        else:
            messages.error(request, "Brak produktów na stanie.")
            return redirect("profile_orders")


@login_required
@transaction.atomic
def order_renew(request, order_id):
    old_order = get_object_or_404(Order, id=order_id, user=request.user)

    p = request.user.profile
    new_order = Order.objects.create(
        user=request.user,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        email=request.user.email,
        phone=request.user.profile.phone,
        address=request.user.profile.address,
        city=request.user.profile.city,
        zip_code=request.user.profile.zip_code,
        country=request.user.profile.country,
    )

    items_to_add = [
        {"product": item.product, "quantity": item.quantity}
        for item in old_order.items.all()
        if item.product.is_available
    ]

    added_count = process_order_items(new_order, items_to_add, request)

    referer_url = request.META.get("HTTP_REFERER", "")
    if added_count > 0:
        if "/profile/orders" in referer_url:
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Zamówienie zostało złożone.",
                },
                status=200,
            )

        else:
            messages.success(request, "Zamówienie zostało złożone.")
            return redirect("profile_orders")

    else:
        transaction.set_rollback(True)
        if "/profile/orders" in referer_url:
            return JsonResponse(
                {"status": "error", "message": "Brak produktów na stanie."}, status=400
            )
        else:
            messages.error(request, "Brak produktów na stanie.")
            return redirect("profile_orders")


@login_required
@require_POST
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ["new", "processing"]:
        order.status = "cancelled"
        order.save()

        return JsonResponse(
            {"status": "success", "message": "Zamówienie zostało anulowane."},
            status=200,
        )
    else:
        return JsonResponse(
            {
                "status": "error",
                "message": "Nie można anulować zamówienia, które zostało już wysłane lub zrealizowane.",
            },
            status=400,
        )

@login_required
def profile_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).all()
    return render(
        request,
        "main/account/wishlist.html",
        {"user": request.user, "wishlist_items": wishlist_items},
    )

def wishlist_add(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        product = get_object_or_404(Product, id=product_id)
        WishlistItem.objects.get_or_create(user=request.user, product=product)

    messages.success(request, f'Produkt "{product.name}" został dodany do listy życzeń!')

    previous_url = request.META.get("HTTP_REFERER")
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect("home")
    
def wishlist_remove(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        product = get_object_or_404(Product, id=product_id)
        WishlistItem.objects.filter(user=request.user, product=product).delete()

    messages.info(request, f'Produkt "{product.name}" został usunięty z listy życzeń.')

    previous_url = request.META.get("HTTP_REFERER")
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect("home")
