from django.urls import path
from .views import PostListView, PostDetailView

app_name = "post"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("<uuid:pk>", PostDetailView.as_view(), name="detail"),
]
