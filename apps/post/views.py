from typing import Any

from common.models import Favorite
from common.serializers import FavoriteSerializer
from common.views import FavoriteUtils
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from utils.paginations import APIPagination

from .models import Post, PostView
from .serializers import PostSerializer
from utils.permissions import IsSellerORRead


class PostListCreateView(ListCreateAPIView):
    permission_classes = [IsSellerORRead]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = APIPagination
    filter_backends = [SearchFilter]
    search_fields = ["headline", "author"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["detail"] = False
        return context


class PostDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_active=True)
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            PostView.objects.get_or_create(user=request.user, post=instance)
        return super().retrieve(request, *args, **kwargs)


class FavouritePostCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type_data = "post.post"
        object_id = request.data.get("object_id")

        return FavoriteUtils.create_favorite(
            self,
            user=request.user,
            content_type_data=content_type_data,
            object_id=object_id,
        )


class FavouritePostDeleteView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSellerORRead]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    # def get_queryset(self):
    #     return

    def delete(self, request, pk, *args, **kwargs):
        return FavoriteUtils.delete_favorite(pk=pk, user=request.user)
