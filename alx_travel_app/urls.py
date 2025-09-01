# alx_travel_app/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse
from alx_travel_app.listings.views import InitiatePaymentView, VerifyPaymentView

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
    # Default homepage
    path("", lambda request: HttpResponse("Welcome to ALX Travel API 🚀")),

    # Django Admin
    path("admin/", admin.site.urls),

    # Listings + Bookings API
    path("listings/", include("alx_travel_app.listings.urls")),

    # Payment endpoints
    path("payments/initiate/", InitiatePaymentView.as_view(), name="initiate-payment"),
    path("payments/verify/<str:tx_ref>/", VerifyPaymentView.as_view(), name="verify-payment"),

    # Swagger & Redoc docs
    re_path(r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
