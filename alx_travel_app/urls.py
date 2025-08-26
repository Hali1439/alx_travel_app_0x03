from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from alx_travel_app.listings.views import InitiatePaymentView, VerifyPaymentView


schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel API",
      default_version='v1',
      description="API documentation for ALX Travel",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('listings/', include('alx_travel_app.listings.urls')),
    path('payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments/verify/<str:tx_ref>/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
