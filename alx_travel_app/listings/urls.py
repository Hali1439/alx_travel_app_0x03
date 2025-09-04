# listings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, InitiatePaymentView, VerifyPaymentView, index

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path("", index, name="listings-index"),  # handles /listings/

    # API routes from DRF router
    path("api/", include(router.urls)),

    # Payment routes (optional duplication for API access)
    path("api/initiate-payment/", InitiatePaymentView.as_view(), name="api-initiate-payment"),
    path("api/verify-payment/<str:tx_ref>/", VerifyPaymentView.as_view(), name="api-verify-payment"),
]
