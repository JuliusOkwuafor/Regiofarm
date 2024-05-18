# Generated by Django 5.0.4 on 2024-05-18 10:53

import django.core.validators
import django.db.models.manager
import uuid
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='seller/', verbose_name='profile photo')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='seller/', verbose_name='cover photo')),
                ('name', models.CharField(max_length=255, verbose_name='company name')),
                ('ceo', models.CharField(max_length=225, verbose_name='company ceo')),
                ('vat', models.CharField(max_length=225, verbose_name='company vat')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('opening_hour', models.TimeField(blank=True, null=True, verbose_name='opening hour')),
                ('closing_hour', models.TimeField(blank=True, null=True, verbose_name='closing hour')),
                ('delivery_terms_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))], verbose_name='delivery price')),
                ('delivery_terms_distance', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True, verbose_name='delivery distance')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='latitude')),
                ('product_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))], verbose_name='discount all product')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_subscribed', models.BooleanField(default=False, verbose_name='is subscribed')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'seller',
                'verbose_name_plural': 'sellers',
                'db_table': 'seller',
                'ordering': ['-created_at'],
            },
            managers=[
                ('is_verified', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SellerCategory',
            fields=[
                ('name', models.CharField(db_index=True, max_length=50, primary_key=True, serialize=False, verbose_name='name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'seller category',
                'verbose_name_plural': 'seller categories',
                'db_table': 'seller_category',
                'ordering': ['name'],
            },
        ),
    ]
