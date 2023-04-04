from celery import shared_task
from django.utils import timezone
from .views import send_expiry_reminder_emails

@shared_task
def send_expiry_reminder_emails_daily():
    send_expiry_reminder_emails(None)  # pass a fake request object
