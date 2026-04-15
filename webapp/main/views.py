
from .models import Product, Profile
from .cart import Cart

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


def index(request):
    products = Product.objects.filter(is_available=True)
    
    return render(request, 'main/index.html', {'products': products})

def contact(request):
    return render(request, "main/contact.html")

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart')

def cart_decrement(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrement(product)
    return redirect('cart')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart')

def cart(request):
    cart = Cart(request)
    return render(request, 'main/cart.html', {'cart': cart})

def about(request):
    return render(request, 'main/about.html')

@login_required
def profile_view(request):
    return render(request, 'main/account/profile.html', {'user': request.user})

# Using the Django authentication system (Django Documentation)
# https://docs.djangoproject.com/en/5.1/topics/auth/default/
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Pomyślnie zalogowano. Cieszymy się, że z nami jesteś!")
            
            if request.session.get('next'):
                return redirect(request.session.pop('next'))
             
            return redirect('home')
        else:
            messages.error(request, "Nieprawidłowy login lub hasło.")
            return redirect('login_user')
         
    if request.GET.get('next'):
        request.session['next'] = request.GET['next']

    return render(request, 'main/account/login.html')

def register(request):
    if request.user.is_authenticated:
         return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)
        
        profile, created = Profile.objects.get_or_create(user=user)
        
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('adress', '') 
        profile.city = request.POST.get('city', '')
        profile.zip_code = request.POST.get('zip_code', '')
        profile.country = request.POST.get('country', 'Polska')
        
        profile.save()
        
        messages.success(request, "Twoje konto zostało pomyślnie utworzone.")
        login(request, user)    
        return redirect('home')
    
    return render(request, 'main/account/register.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Pomyślnie wylogowano. Zapraszamy ponownie!")
    return redirect('home')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Twoje konto zostało pomyślnie usunięte.")
        return redirect('home')
    
    return redirect('profile')

def search(request):
    query = request.GET.get('q', '') 
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(manufacturer__name__icontains=query) | 
            Q(description__icontains=query),
            is_available=True
        )
        
    return render(request, 'main/search.html', {'products': products, 'query': query})