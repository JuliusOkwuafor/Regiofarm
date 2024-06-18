# Generated by Django 5.0.4 on 2024-06-18 14:22

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_order_note_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))], verbose_name='price'),
        ),
    ]
