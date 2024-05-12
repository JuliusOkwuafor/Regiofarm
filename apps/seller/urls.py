from django.urls import path

from .views import (
    FavouriteSellerCreateView,
    FavouriteSellerDeleteView,
    SellerListView,
    SellerView,
)

app_name = "seller"

urlpatterns = [
    path("", SellerListView.as_view(), name="seller"),
    path("<uuid:pk>/", SellerView.as_view(), name="seller"),
    path(
        "favorite/create",
        FavouriteSellerCreateView.as_view(),
        name="favorite_post",
    ),
    path(
        "favorite/delete/<int:pk>/",
        FavouriteSellerDeleteView.as_view(),
        name="unfavorite_post",
    ),
]
