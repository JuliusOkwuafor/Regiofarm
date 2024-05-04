from django.contrib import admin

from .models import OTP, User,UserAddress

# Register your models here.
admin.site.register(User)
admin.site.register(OTP)
admin.site.register(UserAddress)
