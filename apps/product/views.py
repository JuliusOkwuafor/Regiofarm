from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView

from utils.permissions import IsSellerORRead
from utils.paginations import APIPagination

from .models import Product, ProductImage
from .serializers import ProductImageSerializer, ProductSerializer
from django.shortcuts import get_object_or_404
from utils.response import APIResponse
from rest_framework import status, permissions
from rest_framework.request import Request
from .models import FavoriteProduct
from common.serializers import FavoriteSerializer
from common.models import Favorite
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from common.views import FavoriteUtils

# Create your views here.


class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSellerORRead]
    pagination_class = APIPagination

    def get_queryset(self):
        if self.request.method == "GET":
            return Product.objects.filter(is_active=True)
        return Product.objects.all()


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSellerORRead]
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.method == "GET":
            return Product.objects.filter(is_active=True)
        return Product.objects.all()


class ProductImageCreateView(APIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsSellerORRead]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return APIResponse(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                code=20000,
                msg="image successfully created",
            )
        return APIResponse(
            msg="error creating image", status=status.HTTP_400_BAD_REQUEST
        )


class ProductImageDeleteView(APIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsSellerORRead]

    def delete(self, request, pk, img_pk):
        image = get_object_or_404(ProductImage, pk=img_pk, product__pk=pk)
        image.delete()
        return APIResponse(
            msg="image successfully deleted", status=status.HTTP_204_NO_CONTENT
        )


class FavouriteProductCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type_data = "product.product"
        object_id = request.data.get("object_id")

        return FavoriteUtils.create_favorite(
            self,
            user=request.user,
            content_type_data=content_type_data,
            object_id=object_id,
        )


class FavouriteProductDeleteView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def delete(self, request, pk, *args, **kwargs):
        return FavoriteUtils.delete_favorite(pk=pk, user=request.user)
