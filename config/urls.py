from django.contrib import admin
from django.urls import include, path

api_version = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        f"{api_version}/auth/",
        include("apps.authentication.urls", namespace="authentication"),
    ),
]
