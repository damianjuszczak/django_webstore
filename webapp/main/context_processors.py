from .cart import Cart
from django.conf import settings
from .utilities import get_live_exchange_rates

def cart(request):
    #  {{ cart }}
    return {'cart': Cart(request)}

def currency_context(request):
    active_currency = request.session.get('currency', settings.DEFAULT_CURRENCY)
    
    live_rates = get_live_exchange_rates()
    
    return {
        'ACTIVE_CURRENCY': active_currency,
        'AVAILABLE_CURRENCIES': live_rates.keys(), 
    }