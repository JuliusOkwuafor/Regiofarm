from common.models import Favorite, Order
from common.serializers import FavoriteSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView
from user.models import User, UserAddress

from utils.permissions import IsUserORAdmin
from utils.response import APIResponse

from .serializers import UserAddressSerializer, UserSerializer,UserOrderSerializer


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


# class UserFavoriteView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = FavoriteSerializer

#     def get(self, request):
#         favourite = Favorite.objects.filter(user=request.user)
#         serializer = self.serializer_class(favourite, many=True)
#         # data = serializer.data

#         return APIResponse(
#             data=serializer.data,
#             status=status.HTTP_200_OK,
#             msg="favourite fetched successfully",
#             code=20000,
#         )


class UserFavoriteListView(ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class UserOrderListView(ListAPIView):
    serializer_class = UserOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)
