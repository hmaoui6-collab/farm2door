from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product


class ProductTest(TestCase):

    def test_create_product(self):
        user = User.objects.create(username='farmer')

        product = Product.objects.create(
            farmer=user,
            name='Tomato',
            price=10,
            stock=5
        )

        self.assertEqual(product.name, 'Tomato')
