from django.urls import path
from .views import UserView, UserAddressView, UserFavouriteView

app_name = "user"

urlpatterns = [
    path("<uuid:pk>/", UserView.as_view(), name="user"),
    path("favorites", UserFavouriteView.as_view(), name="favorite"),
    # path("address/<uuid:pk>/", UserAddressView.as_view(), name="user_address"),
]
