# alx_travel_app/listings/urls_api.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path("", include(router.urls)),  # /api/listings/, /api/bookings/
    path("payments/initiate/", InitiatePaymentView.as_view(), name="initiate-payment"),
    path("payments/verify/<str:tx_ref>/", VerifyPaymentView.as_view(), name="verify-payment"),
]
