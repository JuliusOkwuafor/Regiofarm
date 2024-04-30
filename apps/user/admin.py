from django.contrib import admin

from .models import OTP, SellerProfile, User

# Register your models here.
admin.site.register(User)
admin.site.register(SellerProfile)
admin.site.register(OTP)
