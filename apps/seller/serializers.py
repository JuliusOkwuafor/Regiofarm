from rest_framework import serializers
from seller.models import Seller
from user.models import User, UserAddress
from user.enums import Role
from common.models import Order
from common.serializers import OrderItemSerializer


class SellerSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Seller
        exclude = ["created_at", "updated_at", "is_active", "is_subscribed"]

    def get_total_likes(self,obj):
        return obj.total_likes()

    def to_representation(self, instance):
        dt = super().to_representation(instance)
        data = {
            "code": 20000,
            "message": "successful",
            "data": dt,
        }
        return data


class SellerOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False, read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    seller_name = serializers.SerializerMethodField(read_only=True)
    seller_profile_image = serializers.ImageField(source='seller.profile_image', read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "owner",
            "seller",
            "seller_name",
            "seller_profile_image",
            "status",
            "tip",
            "items",
            "total",
            "payment_method",
            "note",
            "placed_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
            "tip": {"read_only": True},
            "items": {"read_only": True},
            "total": {"read_only": True},
            "placed_at": {"read_only": True},
        }

    def get_seller_name(self, obj):
        return obj.seller.name

    # def get_seller_image(self, obj):
    #     image_url = obj.seller.profile_image.url
    #     return image_url if image_url else None

    def get_total(self, obj):
        items = obj.order_item.all()
        total = sum([item.quantity * item.price for item in items])
        return total
