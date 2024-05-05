from django.urls import path

from .views import SellerView

app_name = "seller"

urlpatterns = [
    path("<uuid:pk>/", SellerView.as_view(), name="seller"),
]
