# Generated by Django 5.0.4 on 2024-05-18 16:51

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_productcategory_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='total_quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))], verbose_name='total quantity'),
        ),
    ]
