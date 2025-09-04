# alx_travel_app/listings/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ["id", "user", "listing", "rating", "comment", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class ListingSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = ["id", "title", "description", "location", "price_per_night", "created_at", "reviews"]

class BookingSerializer(serializers.ModelSerializer):
    # accept raw IDs on write; return full nested on read (nice DX)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Booking
        fields = ["id", "listing", "user", "check_in", "check_out", "guests"]
