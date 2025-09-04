# alx_travel_app/listings/views.py
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email
import requests, uuid

def index(request):
    # show latest 8 listings on the homepage
    listings = Listing.objects.order_by("-created_at")[:8]
    return render(request, "listings/index.html", {"listings": listings})

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().order_by("-created_at")
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        booking_details = (
            f"Booking ID: {booking.id}\n"
            f"Listing: {booking.listing.title}\n"
            f"Check-in: {booking.check_in}\n"
            f"Check-out: {booking.check_out}\n"
            f"Guests: {booking.guests}"
        )
        send_booking_confirmation_email.delay(booking.user.email, booking_details)

class InitiatePaymentView(APIView):
    def post(self, request):
        booking_reference = request.data.get("booking_reference")
        amount = request.data.get("amount")
        email = request.data.get("email")
        tx_ref = str(uuid.uuid4())

        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": email,
            "tx_ref": tx_ref,
            "callback_url": "https://yourdomain.com/api/payments/verify/",
            "return_url": "https://yourdomain.com/payment-success/",
        }
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            "https://api.chapa.co/v1/transaction/initialize",
            json=payload,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            checkout_url = data["data"]["checkout_url"]
            Payment.objects.create(
                booking_reference=booking_reference,
                transaction_id=tx_ref,
                amount=amount,
                status="Pending",
            )
            return Response({"checkout_url": checkout_url}, status=status.HTTP_200_OK)

        return Response({"error": response.json()}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(APIView):
    def get(self, request, tx_ref):
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        response = requests.get(
            f"https://api.chapa.co/v1/transaction/verify/{tx_ref}",
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            status_code = data["data"]["status"]
            payment = get_object_or_404(Payment, transaction_id=tx_ref)

            if status_code == "success":
                payment.status = "Completed"
                # (optionally) email the user here
            else:
                payment.status = "Failed"

            payment.save()
            return Response({"status": payment.status}, status=status.HTTP_200_OK)

        return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)
