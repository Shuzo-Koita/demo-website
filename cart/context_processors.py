from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    item_count = 0
    total_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                total_count += (cart_item.product.price * cart_item.quantity)
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
            total_count = 0
    return dict(item_count = item_count,total_count = total_count)