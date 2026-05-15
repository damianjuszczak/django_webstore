import requests
from django.core.cache import cache

def get_live_exchange_rates():
    rates = cache.get('live_exchange_rates')
    
    if rates:
        return rates 

    try:
        url = 'https://open.er-api.com/v6/latest/PLN'
        
        #request api
        response = requests.get(url, timeout=5)
        response.raise_for_status() #error if api is down
        data = response.json() #api response into a python dictionary
        
        #filer wanted currencies
        all_rates = data.get('rates', {})
        allowed_currencies = ['PLN', 'EUR', 'USD']

        if not filtered_rates:
            raise ValueError("API returned empty data")
        
        filtered_rates = {k: v for k, v in all_rates.items() if k in allowed_currencies}
        
        #save cache for 1 hour
        cache.set('live_exchange_rates', filtered_rates, 3600)
        
        return filtered_rates
        
        #fallback
    except Exception as e:
        print(f"API Error: {e}")
        return {'PLN': 1.0, 'EUR': 0.23, 'USD': 0.25}