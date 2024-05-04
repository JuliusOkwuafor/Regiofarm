from django.urls import path
from .views import UserView, UserAddressView

app_name = "user"

urlpatterns = [
    path("<uuid:pk>/", UserView.as_view(), name="user"),
    # path("address/<uuid:pk>/", UserAddressView.as_view(), name="user_address"),
]
