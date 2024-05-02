from django.urls import path

from .views import SellerProfileView

app_name = "seller"

urlpatterns = [
    path("<uuid:pk>/", SellerProfileView.as_view(), name="seller_profile"),
]
