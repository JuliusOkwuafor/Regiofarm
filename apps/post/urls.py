from django.urls import path

from .views import (
    FavouritePostCreateView,
    FavouritePostDeleteView,
    PostDetailView,
    PostListView,
)

app_name = "post"

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("<uuid:pk>", PostDetailView.as_view(), name="detail"),
    path(
        "favorite/create",
        FavouritePostCreateView.as_view(),
        name="favorite_post",
    ),
    path(
        "favorite/delete/<int:pk>/",
        FavouritePostDeleteView.as_view(),
        name="unfavorite_post",
    ),
]
