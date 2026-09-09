import resend
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Profile 

@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    if created:
        # 1. Create the blank profile automatically for new register
        Profile.objects.create(user=instance)
        
        # 2. Send the welcome email via Resend API
        if instance.email:
            # telling the sdk to use the password you already set in settings.py
            resend.api_key = settings.EMAIL_HOST_PASSWORD
            
            html_content = render_to_string('emails/welcome.html', {'username': instance.username})
            text_content = strip_tags(html_content)
            
            params = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [instance.email],
                "subject": "Welcome to Project Katha!",
                "html": html_content,
                "text": text_content,
            }
            
            # This sends via standard HTTPS, completely bypassing the SMTP block!
            resend.Emails.send(params)