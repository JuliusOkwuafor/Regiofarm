from rest_framework import serializers
from .models import Favorite
from seller.models import Seller
from product.models import Product
from post.models import Post


class FavoriteSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()
    object_id = serializers.IntegerField(write_only=True)
    content_object = serializers.SerializerMethodField()

    def get_content_object(self, obj):
        content_type = obj.content_type
        model_class = content_type.model_class()
        obj_ = model_class.objects.get(pk=obj.object_id)
        if model_class == Product:
            # model_class:Product
            data = {
                
            }
        elif model_class == Seller:
            # model_class:Seller
            data = {
                "name": f"{obj_.user.firstname} {obj_.user.lastname}",
                "category": obj_.category,
                "city": obj_.user.address.city,
                "total_likes": "total likes",
                "latitude": obj_.latitude,
                "longitude": obj_.longitude,
                "is_opened": obj_.is_open(),
            }
        elif model_class == Post:
            model_class:Post
            data = {
                "headline": obj_.headline,
                "content": obj_.content,
                "link": obj_.link,
                "total_views": obj_.total_views,
                "total_likes": obj_.total_likes,
                "created_at": obj_.created_at,
            }
        else:
            data = {}

        return data

    class Meta:
        model = Favorite
        fields = ["user", "content_type", "object_id", "content_object"]
        extra_kwargs = {"content_object": {"read_only": True}}
