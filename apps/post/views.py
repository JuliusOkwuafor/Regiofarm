from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView,DestroyAPIView
from rest_framework import permissions

from common.models import Favorite
from .serializers import PostSerializer
from .models import Post, PostView
from typing import Any
from common.serializers import FavoriteSerializer
from common.views import FavoriteUtils


class PostListView(ListAPIView):
    authentication_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def delete(self, request, pk, *args, **kwargs):
        return FavoriteUtils.delete_favorite(pk=pk, user=request.user)