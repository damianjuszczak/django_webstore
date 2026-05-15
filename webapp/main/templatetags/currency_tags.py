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
        return f"{converted_price:.2f} {currency}"
    except (ValueError, TypeError):
        return price