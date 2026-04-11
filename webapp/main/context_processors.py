from .cart import Cart

def cart(request):
    #  {{ cart }}
    return {'cart': Cart(request)}