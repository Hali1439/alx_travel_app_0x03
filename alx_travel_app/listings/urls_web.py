# alx_travel_app/listings/urls_web.py
from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name="listings-index"),        # /listings/
]
