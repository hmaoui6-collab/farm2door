from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import connection

from core.models import Product, Profile


class Command(BaseCommand):
    help = "Create demo users and products for Farm2Door."

    def _column_names(self, table_name):
        with connection.cursor() as cursor:
            return [column.name for column in connection.introspection.get_table_description(cursor, table_name)]

    def _check_database_schema(self):
        product_columns = self._column_names('core_product')
        profile_columns = self._column_names('core_profile')

        old_product_schema = 'description' in product_columns or 'created_at' in product_columns
        old_profile_schema = 'role' in profile_columns and 'user_type' not in profile_columns

        if old_product_schema or old_profile_schema:
            self.stdout.write(self.style.ERROR('La base db.sqlite3 utilise encore une ancienne structure.'))
            self.stdout.write('Solution simple pour la demo PFA:')
            self.stdout.write('1. Arreter le serveur Django')
            self.stdout.write('2. Supprimer le fichier db.sqlite3')
            self.stdout.write('3. Relancer: python manage.py migrate')
            self.stdout.write('4. Relancer: python manage.py seed_demo')
            return False

        return True

    def handle(self, *args, **options):
        if not self._check_database_schema():
            return

        farmer, _ = User.objects.get_or_create(
            username='farmer',
            defaults={'email': 'farmer@farm2door.ma'},
        )
        farmer.set_password('farmer123')
        farmer.save()
        Profile.objects.get_or_create(user=farmer, defaults={'user_type': 'farmer'})

        client, _ = User.objects.get_or_create(
            username='client',
            defaults={'email': 'client@farm2door.ma'},
        )
        client.set_password('client123')
        client.save()
        Profile.objects.get_or_create(user=client, defaults={'user_type': 'customer'})

        admin, _ = User.objects.get_or_create(
            username='abdellah',
            defaults={'email': 'abdellah@farm2door.ma', 'is_staff': True, 'is_superuser': True},
        )
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('Anomaly123')
        admin.save()
        Profile.objects.get_or_create(user=admin, defaults={'user_type': 'customer'})

        products = [
            ('Tomates', 8, 40, 'products/maticha.jpg'),
            ('Pommes de terre', 6, 80, 'products/btata.jpg'),
            ('Oignons rouges', 7, 65, 'products/bassla.jpg'),
            ('Carottes', 7, 50, 'products/carotte.jpg'),
            ('Concombres', 5, 45, 'products/concombre.jpg'),
            ('Courgettes', 9, 35, 'products/courgette.jpg'),
            ('Aubergines', 10, 30, 'products/aubergine.jpg'),
            ('Poivron vert', 12, 30, 'products/poivron_vert_jpg.jpg'),
            ('Poivron rouge', 13, 28, 'products/poivron_jpg.jpg'),
            ('Laitue', 5, 25, 'products/laitue_jpg.jpg'),
        ]

        for name, price, stock, image in products:
            product, _ = Product.objects.update_or_create(
                farmer=farmer,
                name=name,
                defaults={'price': price, 'stock': stock, 'image': image},
            )

        self.stdout.write(self.style.SUCCESS('Demo Farm2Door created successfully.'))
