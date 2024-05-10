from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .serializers import PostSerializer
from .models import Post, PostView
from typing import Any


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
