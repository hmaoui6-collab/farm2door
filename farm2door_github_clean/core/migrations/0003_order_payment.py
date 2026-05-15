# Generated for Farm2Door payment workflow.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(
                choices=[('cash', 'Paiement a la livraison'), ('card', 'Carte bancaire')],
                default='cash',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(
                choices=[('pending', 'En attente'), ('paid', 'Paye')],
                default='pending',
                max_length=20,
            ),
        ),
    ]
