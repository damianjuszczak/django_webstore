# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from . import views

urlpatterns = [
    # Standard pages
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name="contact"),
    path('search', views.search, name='search'),


    # Account
    path('login', views.login_user, name='login_user'),
    path('register', views.register, name='register_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('profile', views.profile_view, name='profile_view'),
    path('delete-account/', views.delete_account, name='delete_account'),
    
    # Cart URLs
    path('cart/', views.cart, name="cart"),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/decrement/<int:product_id>/', views.cart_decrement, name='cart_decrement'),
]