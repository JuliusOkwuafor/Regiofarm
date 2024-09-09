from datetime import datetime, timezone

from common.models import Favorite
from common.serializers import FavoriteSerializer
from common.views import FavoriteUtils
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from post.models import Post
from post.serializers import PostSerializer
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from seller.models import Seller

from utils.paginations import APIPagination
from utils.permissions import IsSellerORRead
from common.models import Order
from .serializers import SellerSerializer, SellerOrderSerializer


class IsSellerORRead(permissions.BasePermission):
    message = (
        "You need to be authenticated and a seller to edit your own profile message "
    )

    def has_object_permission(self, request: Request, view, obj: Seller):
        if request.user.is_authenticated:
            return obj.user == request.user
        return False


class SellerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SellerSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAuthenticated, IsSellerORRead]

    def get_queryset(self):
        return Seller.objects.filter(pk=self.kwargs.get(self.lookup_field))


class SellerListView(generics.ListAPIView):
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category"]
    pagination_class = APIPagination
    search_fields = ["name", "user__firstname", "user__lastname", "user__address__city"]
    # schema=''

    def get_queryset(self):
        is_open = self.request.query_params.get("is_open")
        if is_open:
            now = datetime.now(tz=timezone.utc)
            if is_open == "opened":
                queryset = Seller.is_verified.filter(
                    opening_hour__lte=now, closing_hour__gte=now
                )
            elif is_open == "closed":
                queryset = Seller.is_verified.exclude(
                    opening_hour__lte=now, closing_hour__gte=now
                )
        else:
            queryset = Seller.is_verified.all()
        return queryset.select_related("category")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="is_open",
                enum=["opened", "closed"],
                in_=openapi.IN_QUERY,
                description="List all sellers",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FavouriteSellerCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["object_id"],
            properties={
                "object_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="seller ID"
                )
            },
        ),
        operation_description="favorite seller endpoint",
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type_data = "seller.seller"
        object_id = request.data.get("object_id")

        return FavoriteUtils.create_favorite(
            self,
            user=request.user,
            content_type_data=content_type_data,
            object_id=object_id,
        )


class FavouriteSellerDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSellerORRead]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def delete(self, request, pk, *args, **kwargs):
        return FavoriteUtils.delete_favorite(pk=pk, user=request.user)


class SellersProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = APIPagination
    lookup_field = "pk"

    def get_queryset(self):
        seller_id = self.kwargs.get(self.lookup_field)
        return (
            Product.objects.filter(is_active=True, seller__id=seller_id)
            .prefetch_related("images")
            .select_related("seller", "category")
        )


class SellersPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = APIPagination
    lookup_field = "pk"

    def get_queryset(self):
        seller_id = self.kwargs.get(self.lookup_field)
        return Post.objects.filter(author__id=seller_id).select_related("author")


class SellersOrderList(generics.ListAPIView):
    serializer_class = SellerOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]
    pagination_class = APIPagination
    lookup_field = "pk"

    def get_queryset(self):
        seller_id = self.kwargs.get(self.lookup_field)
        return Order.objects.filter(seller__id=seller_id)


class SellersOrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        seller_id = self.kwargs.get("pk")
        order_id = self.kwargs.get("order_id")
        return Order.objects.filter(seller__id=seller_id, id=order_id)
