from django.urls import path
from .views import OrderCreateView,OrderDetailView

app_name = "common"

urlpatterns = [
    path("orders/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<uuid:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
