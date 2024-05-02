from rest_framework import serializers
from user.models import User
from seller.models import SellerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "firstname", "lastname", "photo", "role")

    def to_representation(self, instance):
        dt = super().to_representation(instance)
        data = {
            "code": 20000,
            "message": "successful",
            "data": dt,
        }
        return data
