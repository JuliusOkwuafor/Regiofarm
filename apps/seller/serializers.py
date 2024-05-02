from rest_framework import serializers
from seller.models import SellerProfile


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        exclude = ["created_at", "updated_at"]

    def to_representation(self, instance):
        dt = super().to_representation(instance)
        data = {
            "code": 20000,
            "message": "successful",
            "data": dt,
        }
        return data
