# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from . import views

urlpatterns = [
    # Standard pages
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name="contact"),
    path('search', views.search, name='search'),
    path('product/<slug:slug>/', views.product_details, name='product_details'),

    path('categories/<slug:category_slug>/', views.category_details, name='category_details'),

    # Auth
    path('login/', views.login_form, name='login_form'),
    path('register/', views.register_form, name='register_form'),
    path('api/auth/login/', views.auth_login, name='login_user'),
    path('api/auth/register/', views.auth_register, name='register_user'),
    path('api/auth/logout/', views.auth_logout, name='logout_user'),

    # Account
    path('profile/', views.profile_info, name='profile_info'),
    path('profile/orders/', views.profile_orders, name='profile_orders'),
    path('profile/reports/', views.profile_reports, name='profile_reports'),
    path('api/profile/delete/', views.profile_delete, name='profile_delete'),
    
    # Cart URLs
    path('cart/', views.cart, name="cart"),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/decrement/<int:product_id>/', views.cart_decrement, name='cart_decrement'),

    # Checkout URLs
    path('checkout/', views.checkout, name='checkout')
]