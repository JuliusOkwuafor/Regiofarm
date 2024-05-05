from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductImageCreateView,
    ProductImageDeleteView,
    FavouriteProductView,
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
        "<uuid:pk>/favourite/", FavouriteProductView.as_view(), name="favourite_produce"
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
