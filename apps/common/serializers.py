from rest_framework import serializers
from .models import Favorite
from seller.models import Seller
from product.models import Product
from post.models import Post
from django.shortcuts import get_object_or_404


class FavoriteSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(
        read_only=True
    )  # Get content type as string representation
    object_id = serializers.UUIDField(read_only=True)
    content_object = serializers.SerializerMethodField()

    def get_content_object(self, obj):
        content_type = obj.content_type
        model_class = content_type.model_class()
        obj_ = model_class.objects.get(pk=obj.object_id)
        if model_class == Product:
            # model_class: Product
            data = {
                "id": obj_.id,
                "name": obj_.name,
                "seller_name": obj_.seller_name,
                "quantity": obj_.quantity,
                "unit": obj_.quantity_unit,
                "price": obj_.price,
                "currency": obj_.currency,
                "total_left": obj_.total_quantity,
            }
        elif model_class == Seller:
            model_class: Seller
            data = {
                "name": obj_.user.full_name,
                "category": obj_.category.name,
                "city": obj_.user.address.city,
                "total_likes": obj_.total_likes(),
                "latitude": obj_.latitude,
                "longitude": obj_.longitude,
                "is_opened": obj_.is_open,
            }
        elif model_class == Post:
            # model_class:Post
            data = {
                "headline": obj_.headline,
                "content": obj_.content,
                "link": obj_.link,
                "total_views": obj_.total_views,
                "total_likes": obj_.total_likes(),
                "created_at": obj_.created_at,
            }
        else:
            data = {}

        return data

    class Meta:
        model = Favorite
        fields = ["id", "user", "content_type", "object_id", "content_object"]
        extra_kwargs = {
            "id": {"read_only": True},
            "content_object": {"read_only": True},
            "user": {"read_only": True},
            "content_type": {"read_only": True},
            "object_id": {"read_only": True},
        }
