from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteListView(ListAPIView):
    serializer_class = FavoriteSerializer
    authentication_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
