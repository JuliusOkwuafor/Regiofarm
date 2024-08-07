from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Regio API",
        default_version="v1",
        description="Regio Backend Documentation",
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
        f"{api_version}/swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        f"{api_version}/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        f"{api_version}/auth/",
        include("apps.authentication.urls", namespace="authentication"),
    ),
    path(
        f"{api_version}/users/",
        include("apps.user.urls", namespace="user"),
    ),
    path(f"{api_version}/sellers/", include("apps.seller.urls", namespace="seller")),
    path(f"{api_version}/products/", include("product.urls", namespace="product")),
    path(f"{api_version}/posts/", include("post.urls", namespace="post")),
    path(
        f"{api_version}/notifications/",
        include("notification.urls", namespace="notification"),
    ),
    path(f"{api_version}/", include("common.urls", namespace="common")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
