from common.models import Favorite
from common.serializers import FavoriteSerializer
from common.views import FavoriteUtils
from rest_framework import generics, permissions
from seller.models import Seller

from utils.permissions import IsSellerORRead

from .serializers import SellerSerializer

# Create your views here.


class SellerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    lookup_field = "pk"
    permission_classes = [IsSellerORRead]

    def get_queryset(self):

        return super().get_queryset()


class SellerListView(generics.ListAPIView):
    serializer_class = SellerSerializer
    queryset = Seller.is_verified.all()
    permission_classes = [permissions.IsAuthenticated]


class FavouriteSellerCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def delete(self, request, pk, *args, **kwargs):
        return FavoriteUtils.delete_favorite(pk=pk, user=request.user)
