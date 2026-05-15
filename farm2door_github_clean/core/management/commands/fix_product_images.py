from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import Product, Profile


class Command(BaseCommand):
    help = "Attach local product photos to Farm2Door products and create missing demo products."

    PRODUCTS = [
        {
            'names': ['tomates', 'tomate', 'maticha'],
            'display': 'Tomates',
            'price': 8,
            'stock': 40,
            'image': 'products/maticha.jpg',
        },
        {
            'names': ['pommes de terre', 'pomme de terre', 'btata'],
            'display': 'Pommes de terre',
            'price': 6,
            'stock': 80,
            'image': 'products/btata.jpg',
        },
        {
            'names': ['oignons rouges', 'oignon rouge', 'oignons', 'bassla'],
            'display': 'Oignons rouges',
            'price': 7,
            'stock': 65,
            'image': 'products/bassla.jpg',
        },
        {
            'names': ['carottes', 'carotte'],
            'display': 'Carottes',
            'price': 7,
            'stock': 50,
            'image': 'products/carotte.jpg',
        },
        {
            'names': ['concombres', 'concombre'],
            'display': 'Concombres',
            'price': 5,
            'stock': 45,
            'image': 'products/concombre.jpg',
        },
        {
            'names': ['courgettes', 'courgette'],
            'display': 'Courgettes',
            'price': 9,
            'stock': 35,
            'image': 'products/courgette.jpg',
        },
        {
            'names': ['aubergines', 'aubergine'],
            'display': 'Aubergines',
            'price': 10,
            'stock': 30,
            'image': 'products/aubergine.jpg',
        },
        {
            'names': ['poivron vert', 'poivrons verts'],
            'display': 'Poivron vert',
            'price': 12,
            'stock': 30,
            'image': 'products/poivron_vert_jpg.jpg',
        },
        {
            'names': ['poivron rouge', 'poivrons rouges', 'poivron'],
            'display': 'Poivron rouge',
            'price': 13,
            'stock': 28,
            'image': 'products/poivron_jpg.jpg',
        },
        {
            'names': ['laitue', 'salade'],
            'display': 'Laitue',
            'price': 5,
            'stock': 25,
            'image': 'products/laitue_jpg.jpg',
        },
    ]

    def handle(self, *args, **options):
        farmer, _ = User.objects.get_or_create(
            username='farmer',
            defaults={'email': 'farmer@farm2door.ma'},
        )
        farmer.set_password('farmer123')
        farmer.save()
        Profile.objects.get_or_create(user=farmer, defaults={'user_type': 'farmer'})

        fixed = 0
        created = 0

        for item in self.PRODUCTS:
            product = None
            for name in item['names']:
                product = Product.objects.filter(name__iexact=name).first()
                if product:
                    break

            if product:
                product.name = item['display']
                product.price = item['price']
                if product.stock <= 0:
                    product.stock = item['stock']
                product.farmer = farmer
                product.image = item['image']
                product.save()
                fixed += 1
            else:
                Product.objects.create(
                    farmer=farmer,
                    name=item['display'],
                    price=item['price'],
                    stock=item['stock'],
                    image=item['image'],
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Images fixed: {fixed}. Products created: {created}.'))
