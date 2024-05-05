from rest_framework import serializers
from .models import Product, ProductImage, FavoriteProduct


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "order"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    new_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "is_active"]

    def get_new_price(self, obj):
        return obj.new_price()

    def to_representation(self, instance):
        dt = super().to_representation(instance)
        data = {
            "code": 20000,
            "message": "successful",
            "data": dt,
        }
        print("jj")
        return data


class FavouriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ["product"]
