from django.urls import path

from .views import (
    FavouriteProductCreateView,
    ProductDetailView,
    ProductImageCreateView,
    ProductImageDeleteView,
    ProductListCreateView,
    FavouriteProductDeleteView,
)

app_name = "product"

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="list-create"),
    path("<uuid:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path(
        "<uuid:pk>/image/",
        ProductImageCreateView.as_view(),
        name="product_image_create",
    ),
    path(
        "<uuid:pk>/image/<str:image_pk>",
        ProductImageDeleteView.as_view(),
        name="product_image_delete",
    ),
    path(
        "favorite/create",
        FavouriteProductCreateView.as_view(),
        name="favorite_product",
    ),
    path(
        "favorite/delete/<int:pk>/",
        FavouriteProductDeleteView.as_view(),
        name="unfavorite_product",
    ),
    # path('', ProductListAPIView.as_view(), name='list'),
    # path('<uuid:pk>/', ProductDetailAPIView.as_view(), name='detail'),
    # path('create/', ProductCreateAPIView.as_view(), name='create'),
    # path('update/<uuid:pk>/', ProductUpdateAPIView.as_view(), name='update'),
    # path('delete/<uuid:pk>/', ProductDeleteAPIView.as_view(), name='delete'),
    # path('favorite/', FavoriteProductListAPIView.as_view(), name='favorite'),
    # path('favorite/create/', FavoriteProductCreateAPIView.as_view(), name='favorite-create'),
    # path('favorite/delete/<uuid:pk>/', FavoriteProductDeleteAPIView.as_view(), name='favorite-delete'),
]
