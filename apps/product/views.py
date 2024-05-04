from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView

from utils.permissions import IsSellerORRead

from .models import Product, ProductImage
from .serializers import ProductImageSerializer, ProductSerializer
from django.shortcuts import get_object_or_404
from utils.response import APIResponse
from rest_framework import status

# Create your views here.


class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSellerORRead]

    def get_queryset(self):
        if self.request.GET:
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
