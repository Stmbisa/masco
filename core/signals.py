from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog, Subscription

@receiver(post_save, sender=Blog)
def send_email_on_new_post(sender, instance, **kwargs):
    subscribers = Subscription.objects.all()
    if subscribers:
        subject = 'New blog post published!'
        message = f"A new blog post '{instance.title}' has been published. Check it out at {instance.get_absolute_url()}."
        from_email = 'noreply@example.com'
        recipient_list = [s.email for s in subscribers]
        send_mail(subject, message, from_email, recipient_list)
