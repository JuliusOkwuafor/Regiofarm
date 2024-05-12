from rest_framework import serializers
from seller.models import Seller
from user.models import User, UserAddress
from user.enums import Role


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        exclude = ["created_at", "updated_at",'is_active','is_subscribed']

    def to_representation(self, instance):
        dt = super().to_representation(instance)
        data = {
            "code": 20000,
            "message": "successful",
            "data": dt,
        }
        return data
