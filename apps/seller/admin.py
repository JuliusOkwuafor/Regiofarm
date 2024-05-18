from django.contrib import admin

from .models import Seller,SellerCategory

# Register your models here.
admin.site.register(SellerCategory)
admin.site.register(Seller)
