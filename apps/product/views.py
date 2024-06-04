from common.models import Favorite
from common.serializers import FavoriteSerializer
from common.views import FavoriteUtils
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.request import Request
from rest_framework.views import APIView

from utils.paginations import APIPagination
from utils.permissions import IsSellerORRead
from utils.response import APIResponse

from .models import Product, ProductImage
from .serializers import ProductImageSerializer, ProductSerializer


class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsSellerORRead]
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
    permission_classes = [permissions.IsAuthenticated, IsSellerORRead]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.all()

    def delete(self, request, pk, *args, **kwargs):
        return FavoriteUtils.delete_favorite(pk=pk, user=request.user)
