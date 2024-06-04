from django.urls import path

from .views import (
    FavouriteSellerCreateView,
    FavouriteSellerDeleteView,
    SellerListView,
    SellersOrderDetailView,
    SellersOrderList,
    SellersPostListView,
    SellersProductListView,
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
    path(
        "<uuid:pk>/products", SellersProductListView.as_view(), name="seller_products"
    ),
    path("<uuid:pk>/posts", SellersPostListView.as_view(), name="seller_products"),
    path("<uuid:pk>/orders", SellersOrderList.as_view(), name="seller_order"),
    path("<uuid:pk>/orders/<uuid:order_id>", SellersOrderDetailView.as_view(), name="seller_order"),

]
