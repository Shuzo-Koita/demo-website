from django.test import TestCase
from django.utils import timezone
 
from shop.models import Category, Product
from cart.models import Cart, CartItem
 
 
class ModelTest(TestCase):
 
    def test_create_cart(self):
        Cart.objects.create(
            cart_id='USERONLY',
            date_added=timezone.now)
 
        c = Cart.objects.all()[0]
        assert str(c) == c.cart_id
 
    def test_create_cartitem(self):
        category = Category.objects.create(
            name='Black Urban Cushion',
            slug='black-urban-cushion',
            description='This is a category for black urban cushion')
 
        product = Product.objects.create(
            name='pag dog',
            slug='pag-dog',
            description='Pag dog is as big as cats',
            category=category,
            price=30.2,
            stock=30,
            available=True)
 
        cart = Cart.objects.create(
            cart_id='USERONLY',
            date_added=timezone.now)
 
        CartItem.objects.create(
            product = product,
            cart=cart,
            quantity=3,
            active=True)
 
        cart_item = CartItem.objects.all()[0]
        assert str(cart_item) == cart_item.product.name