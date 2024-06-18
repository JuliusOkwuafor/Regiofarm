from django.contrib import admin

from .models import Favorite, Order, OrderItem

admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
