from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(user_email, booking_details):
    subject = "Booking Confirmation"
    message = f"Hello,\n\nYour booking has been confirmed:\n\n{booking_details}\n\nThank you for using ALX Travel App!"
    sender = settings.EMAIL_HOST_USER
    recipient = [user_email]

    send_mail(subject, message, sender, recipient)
    return f"Confirmation email sent to {user_email}"
