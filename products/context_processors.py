from .cart import Cart

def cart_total_items(request):
    cart = Cart(request)
    total_items = len(cart) if request.user.is_authenticated else 0
    return {'cart_total_items': total_items}