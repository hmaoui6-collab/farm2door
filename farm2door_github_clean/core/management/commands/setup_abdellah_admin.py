from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import Profile


class Command(BaseCommand):
    help = "Create Abdellah as the main admin and disable the old demo admin account."

    def handle(self, *args, **options):
        abdellah, _ = User.objects.get_or_create(
            username='abdellah',
            defaults={'email': 'abdellah@farm2door.ma'},
        )
        abdellah.is_staff = True
        abdellah.is_superuser = True
        abdellah.is_active = True
        abdellah.set_password('Anomaly123')
        abdellah.save()
        Profile.objects.get_or_create(user=abdellah, defaults={'user_type': 'customer'})

        old_admin = User.objects.filter(username='admin').first()
        if old_admin and old_admin.id != abdellah.id:
            old_admin.is_staff = False
            old_admin.is_superuser = False
            old_admin.is_active = False
            old_admin.save()

        self.stdout.write(self.style.SUCCESS('Admin principal configure: abdellah / Anomaly123'))
