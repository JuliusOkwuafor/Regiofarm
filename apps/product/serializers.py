from rest_framework import serializers
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

    def get_new_price(self, obj):
        return obj.new_price

    def create(self, validated_data):
        images = validated_data.pop("upload_images")
        product = Product.objects.create(**validated_data)
        order = 0
        for image in images:
            ProductImage.objects.create(product=product, image=image, order=order)
            order += 1
        return product

    def to_representation(self, instance):
        dt = super().to_representation(instance)
        data = {
            "code": 20000,
            "message": "successful",
            "data": dt,
        }
        print("jj")
        return data
