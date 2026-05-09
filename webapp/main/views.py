
from .models import Product, Profile, Category, Order, OrderItem
from .cart import Cart
from .contact import ContactForm

from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.db import transaction, IntegrityError
from django.views.decorators.http import require_POST


def index(request):
    products = Product.objects.filter(is_available=True).order_by('?')[:4]
    return render(request, 'main/index.html', {'products': products})


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
        return JsonResponse({"status": "error", "message": "Błędne dane logowania"}, status=401)

@require_POST
def auth_register(request):
    if request.user.is_authenticated:
        messages.error(request, "Wyloguj się i spróbuje ponownie zarejestrować nowe konto.")
        return JsonResponse({"status": "success", "redirect_url": "/"})

    try:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        profile, created = Profile.objects.get_or_create(user=user)
        
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '') 
        profile.city = request.POST.get('city', '')
        profile.zip_code = request.POST.get('zip_code', '')
        profile.country = request.POST.get('country', 'Polska')
        
        profile.save()

        login(request, user)
        messages.success(request, "Twoje konto zostało pomyślnie utworzone.")
        return JsonResponse({"status": "success", "redirect_url": "/profile/"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Ten login jest już zajęty."}, status=400)
    except Exception:
        return JsonResponse({"status": "error", "message": "Coś poszło nie tak podczas rejestracji."}, status=500)

@require_POST
def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Pomyślnie wylogowano.")
        return JsonResponse({"status": "success", "redirect_url": "/"})
    return JsonResponse({"status": "success", "redirect_url": "/"})

@login_required
def profile_info(request):
    return render(request, "main/account/profile_info.html", {
        'user': request.user,
        "active_tab": "info"
    })

@login_required
def profile_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items_products")
    return render(request, "main/account/profile_orders.html", {
        "user": request.user, 
        "orders": orders,
        "active_tab": "orders"
    })
            
@login_required
def profile_reports(request):
    return render(request, "main/account/profile_reports.html", {
        "user": request.user,
        "active_tab": "reports"
    })

@login_required
@require_POST
def profile_delete(request):
    try:
        user = request.user
        user.delete()
        return JsonResponse({
            "status": "success",
            "message": "Twoje konto zostało pomyślnie usunięte.",
            "redirect_url": "/"
        }, status=200)
    
    except Exception as e:
        messages.error(request, "Wystąpił nieoczekiwany błąd. Nie udało się usunąć konta.")
        return JsonResponse({
            "status": "error",
            "message": "Nie udało się usunąc konta."
        }, status=500)

@transaction.atomic
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Twój koszyk jest pusty.")
        return redirect('cart_view')

    order = Order.objects.create(
        user=request.user,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        email=request.user.email,
        phone="user.profile.phone",
        address="user.profile.address",
        city="user.profile.city",
        zip_code="user.profile.zip_code",
        country="user.profile.country",
    )

    items_added = 0

    for item in cart:
        product = item['product']
        quantity = item['quantity']
        price = product.price

        updated = Product.objects.filter(
            id=product.id, 
            stock__gte=quantity
        ).update(stock=F('stock') - quantity)

        if updated:
            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                quantity=quantity
            )
            items_added += 1
        else:
            messages.warning(request, f"Produkt {product.name} jest niedostępny w wybranej ilości.")

    if items_added > 0:
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, "Zamówienie zostało złożone pomyślnie!")
    else:
        transaction.set_rollback(True)

    return redirect('cart')
