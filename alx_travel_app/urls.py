# alx_travel_app/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from alx_travel_app.listings.views import index  # reuse as homepage if you like

schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel API",
        default_version="v1",
        description="API documentation for ALX Travel App",
        terms_of_service="https://www.alxafrica.com/",
        contact=openapi.Contact(email="support@alxtravel.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", index, name="home"),                                  # /
    path("admin/", admin.site.urls),                               # /admin/
    path("listings/", include("alx_travel_app.listings.urls_web")),# /listings/
    path("api/", include("alx_travel_app.listings.urls_api")),     # /api/...
    path('api-auth/', include('rest_framework.urls')),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
