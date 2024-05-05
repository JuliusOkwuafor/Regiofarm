from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

from utils.permissions import IsSellerORRead
from utils.paginations import APIPagination

from .models import Product, ProductImage
from .serializers import (
    ProductImageSerializer,
    ProductSerializer,
    FavouriteProductSerializer,
)
from django.shortcuts import get_object_or_404
from utils.response import APIResponse
from rest_framework import status, permissions
from rest_framework.request import Request
from .models import FavoriteProduct

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


class FavouriteProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavouriteProductSerializer

    def post(self, request: Request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return APIResponse(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                code=20000,
                msg="product successfully added to favourite",
            )
        return APIResponse(
            msg="error adding product to favourite", status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        favourite = get_object_or_404(
            FavoriteProduct, user=request.user, product=product
        )
        favourite.delete()
        return APIResponse(
            msg="product successfully deleted from favourite",
            status=status.HTTP_204_NO_CONTENT,
            code=20000,
        )

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsSellerORRead]
        return super().get_permissions()

    def get(self, request, pk):
        product = get_object_or_404(FavoriteProduct, product__pk=pk)
        serializer = self.serializer_class(product, many=True)
        return APIResponse(
            data=serializer.data,
            status=status.HTTP_200_OK,
            code=20000,
            msg="favourite product list",
        )
