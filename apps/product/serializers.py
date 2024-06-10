from rest_framework import serializers

from seller.models import Seller
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "order"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    new_price = serializers.SerializerMethodField(read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=True),
        write_only=True,
    )

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "is_active"]
        extra_kwargs = {
            "id": {"read_only": True},
            "seller": {"read_only": True},
        }

    def get_new_price(self, obj):
        return obj.new_price


    def create(self, validated_data):
        role = self.context.get("request").user.role == 'seller'
        # import pdb;pdb.set_trace()
        if role:
            seller = self.context["request"].user.seller
            images = validated_data.pop("upload_images")
            product = Product.objects.create(seller=seller, **validated_data)
            order = 0
            for image in images:
                ProductImage.objects.create(product=product, image=image, order=order)
                order += 1
            return product
        raise serializers.ValidationError('only a seller can access this endpoint')

    def to_representation(self, instance):
        dt = super().to_representation(instance)
        data = {
            "code": 20000,
            "message": "successful",
            "data": dt,
        }
        return data
