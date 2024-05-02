from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Regio API",
        default_version="v1",
        #   description="Test description",
        #   terms_of_service="https://www.google.com/policies/terms/",
        #   contact=openapi.Contact(email="contact@snippets.local"),
        #   license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


api_version = "api/v1"

urlpatterns = [
    path(
        f"{api_version}/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path(
        f"{api_version}/auth/",
        include("apps.authentication.urls", namespace="authentication"),
    ),
    path(
        f"{api_version}/users/",
        include("apps.user.urls", namespace="user"),
    ),
    path(f"{api_version}/sellers/", include("apps.seller.urls", namespace="seller")),
]
