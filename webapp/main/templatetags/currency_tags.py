import math

from django import template
from django.conf import settings
from main.utilities import get_live_exchange_rates 

register = template.Library()

@register.simple_tag(takes_context=True)
def convert_price(context, price):
    request = context.get('request')
    currency = request.session.get('currency', settings.DEFAULT_CURRENCY)
    
    live_rates = get_live_exchange_rates()
    
    rate = live_rates.get(currency, 1.0)
    
    try:
        converted_price = float(price) * float(rate)
        
        if currency == settings.DEFAULT_CURRENCY:
            #pln is not affected
            final_price = converted_price
        else:
            # .99
            final_price = math.ceil(converted_price) - 0.01
            
        return f"{final_price:.2f} {currency}"
    except (ValueError, TypeError):
        return price