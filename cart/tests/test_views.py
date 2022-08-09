from django.test import TestCase
from django.urls import reverse
 
 
CART_DETAIL_URL = reverse('cart:cart_detail')
 
 
class ViewTest(TestCase):
 
    def test_correct_urls(self):
        response = self.client.get(CART_DETAIL_URL)
        assert response.status_code == 200