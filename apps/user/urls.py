from django.urls import path

from .views import UserAddressView, UserFavoriteListView, UserOrderListView, UserView

app_name = "user"

urlpatterns = [
    path("<uuid:pk>", UserView.as_view(), name="user"),
    path("favorites", UserFavoriteListView.as_view(), name="favorite"),
    path("orders", UserOrderListView.as_view(), name="user-order"),
    # path("address/<uuid:pk>/", UserAddressView.as_view(), name="user_address"),
]
