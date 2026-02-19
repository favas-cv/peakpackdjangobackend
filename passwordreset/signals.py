from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
@receiver(reset_password_token_created)
def password_reset_token_sending(sender,instance,reset_password_token,*args,**kwargs):
    
    reset_link = f"http://localhost:3000/reset-password/{reset_password_token.key}"
    send_mail(
        "password Reset for PeakPack,"
        f"Click the link for rest your password : {reset_link}",
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
        fail_silently=True
    )
    
    