from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = 'Welcome to Project Katha!'
        
        # Load the custom HTML template and pass the username to it
        html_content = render_to_string('emails/welcome.html', {'username': instance.username})
        
        # Create a plain text fallback version just in case an email client blocks HTML
        text_content = strip_tags(html_content)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
            html_message=html_content,
        )