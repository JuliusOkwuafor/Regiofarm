from common.models import Favorite
from common.serializers import FavoriteSerializer
from common.views import FavoriteUtils
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from utils.paginations import APIPagination
from utils.permissions import IsSellerORRead

from .models import Post, PostImage, PostView
from .serializers import PostSerializer


class PostListCreateView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSellerORRead]
    serializer_class = PostSerializer
    pagination_class = APIPagination
    filter_backends = [SearchFilter]
    search_fields = ["headline", "author"]

    def get_queryset(self):
        if self.request.method == "GET":
            return (
                Post.objects.prefetch_related(
                    "images",
                    "post_view",
                    "author",
                    "author__user",
                    "author__user__address",
                )
                .filter(is_active=True)
                .select_related("author")
            )
        return Post.objects.filter(is_active=True)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticated]
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["object_id"],
            properties={
                "object_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Post ID"
                )
            },
        ),
        operation_description="favorite post endpoint",
    )
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
