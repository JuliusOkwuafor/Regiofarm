from rest_framework import serializers
from .models import Favorite
from seller.models import Seller
from product.models import Product
from post.models import Post
from .models import Order, OrderItem


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


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "product_name", "quantity", "price"]
        extra_kwargs = {
            "id": {"read_only": True},
            "product_name": {"read_only": True},
        }

    def save(self, **kwargs):
        order_id = self.validated_data["order"]
        product_id = self.validated_data["product"]
        quantity = self.validated_data["quantity"]
        try:
            order_item = OrderItem.objects.get(
                product__id=product_id, order__id=order_id
            )
            order_item.quantity += quantity
            order_item.save()
            self.instance = order_item
        except OrderItem.DoesNotExist:
            validated_data = self.validated_data
            self.instance = OrderItem.objects.create(**validated_data)

        return self.instance


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "owner",
            "seller",
            "status",
            "tip",
            "items",
            # "order_item",
            "total",
            "payment_method",
            "note",
            "placed_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
            "note": {"read_only": True},
        }

    def create(self, validated_data):
        order_items = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)
        for item_data in order_items:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def get_total(self, obj: Order):
        items = obj.order_item.all()
        total = sum([item.quantity * item.price for item in items])
        return total
