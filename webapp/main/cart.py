from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        
        # If the cart exists but has old dictionary data, reset it to empty
        if cart:
            for key, value in cart.items():
                if type(value) is dict:
                    cart = None # Destroy the old corrupted cart
                    break
        
        if not cart:
            cart = self.session['cart'] = {}
            
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        
        # Add the product or increase its quantity
        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1
            
        # FORCE Django to save the session by explicitly overwriting it
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            # FORCE Django to save the session
            self.session['cart'] = self.cart
            self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            quantity = self.cart[str(product.id)]
            yield {
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            }

    def __len__(self):
        return sum(self.cart.values())

    def get_total_price(self):
        total = 0
        for item in self:
            total += item['total_price']
        return total