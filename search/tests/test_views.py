from django.test import Client
from django.test import TestCase
from django.urls import reverse
 
# new
from shop.models import Category, Product
 
 
SEARCH_RESULT_URL = reverse('search:search_result')
 
# new
def sample_category(name, slug, description):
    return  Category.objects.create(
        name=name,
        slug=slug,
        description=description)
 
# new
def sample_product(name, slug, description, category, price, stock, available, image="test.png"):
    return Product.objects.create(
        name=name,
        slug=slug,
        description=description,
        category=category,
        price=price,
        stock=stock,
        available=available)
 
class SearchTest(TestCase):
    # new
    def setUp(self):
       
        self.client = Client()
 
        self.category = sample_category(
            name='Black Urban Cushion',
            slug='black-urban-cushion',
            description='This is a category for black urban cushion')
 
        self.product1  = sample_product(
             name='dog',
             slug='dog',
             description='Dogs are intelligent animals!',
             category=self.category,
             price=30.2,
             stock=30,
             available=True)
 
        self.product2  = sample_product(
             name='cat',
             slug='cat',
             description='cats are so cute animal!',
             category=self.category,
             price=30.2,
             stock=30,
             available=True)
 
        self.product3  = sample_product(
             name='rabbit',
             slug='rabbit',
             description='Rabbits are small animals!',
             category=self.category,
             price=30.2,
             stock=30,
             available=True)
 
    def test_access_to_search_result_view(self):
        response = self.client.get(SEARCH_RESULT_URL)
        assert response.status_code == 200
 
    # new
    def test_search_result(self):
        response = self.client.get(SEARCH_RESULT_URL, {'q': 'dog'})
 
        assert 'dog' in [product.name for product in response.context['products']]
        assert 'rabbit' not in [product.name for product in response.context['products']]
        assert 'cat' not in [product.name for product in response.context['products']]