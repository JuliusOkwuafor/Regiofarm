from rest_framework.views import APIView
from utils.permissions import IsUserORAdmin
from rest_framework import generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from utils.response import APIResponse

from .serializers import UserSerializer, UserAddressSerializer
from user.models import User, UserAddress


class UserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"
    permission_classes = [IsUserORAdmin]


class UserAddressView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    lookup_field = "pk"
    permission_classes = (IsUserORAdmin,)

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)

    # @swagger_auto_schema(operation_summary="")
    # def perform_destroy(self, instance):
    #     return self.perform_destroy(instance)

    # @swagger_auto_schema(operation_summary="")
    # def retrieve(self, request, *args, **kwargs):
    #     response = super().retrieve(request, *args, **kwargs)

    #     if isinstance(response, Response):
    #         data = {"data": response.data}

    #         return Response(data)

    # @swagger_auto_schema(operation_summary="")
    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)
