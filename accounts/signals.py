from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings

@receiver(post_save,sender=User)
def welcome_mail(sender,instance,created,**kwargs):
    
    subject = "Adventure Confirmed – Welcome to PeakPack "

    message = (
    f"Hi {instance.username},\n\n"
    "Welcome to PeakPack – where every journey begins with purpose.\n\n"
    "Your account has been successfully created, and you're now part of a community "
    "that lives for adventure, exploration, and reaching new heights.\n\n"
    "At PeakPack, we believe in one thing:\n"
    "Pack for the Peaks.\n\n"
    "Gear up with confidence. Explore without limits. Conquer every trail.\n\n"
    "You can now log in using your email and password to start discovering premium "
    "trekking essentials crafted for your next adventure.\n\n"
    "The mountains are calling — and your journey starts here.\n\n"
    "Stay bold,\n"
    "Team PeakPack 🏕️"
)

    
    if created:
        send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=True
        )
        
@receiver(post_delete,sender=User)
def delete_mail(sender,instance,**kwargs):
    
    subject = "Your PeakPack Account Has Been Removed"

    message = (
    f"Hi {instance.username},\n\n"
    "This is to inform you that your PeakPack account has been permanently removed "
    "following an administrative review.\n\n"
    "As part of our commitment to maintaining a safe and reliable adventure community, "
    "certain actions may result in account removal in accordance with our policies.\n\n"
    "If you believe this decision was made in error, you may reach out to our support team "
    "for further clarification.\n\n"
    "We appreciate the time you spent with PeakPack.\n\n"
    "Pack for the Peaks.\n\n"
    "Team PeakPack 🏔️"
)

    
    if instance.email:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True

        )
    
    
    
from urllib.parse import quote
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_sending(sender, instance, reset_password_token, *args, **kwargs):

    # 1️⃣ Generate safe token
    token = quote(reset_password_token.key.strip())

    # 2️⃣ Build reset link
    reset_link = f"http://127.0.0.1:5173/resetpassword?token={token}"

    print("RESET LINK:", reset_link)  # Debug only

    # 3️⃣ Email subject
    subject = "Password Reset for PeakPack"

    # 4️⃣ Plain text fallback
    text_content = f"Click the link below to reset your password:\n{reset_link}"

    # 5️⃣ HTML content (NO line wrapping issue)
    html_content = f"""
    <p>Hello,</p>
    <p>Click the button below to reset your password:</p>
    <p>
        <a href="{reset_link}" 
           style="background-color:#16a34a;
                  color:white;
                  padding:10px 20px;
                  text-decoration:none;
                  border-radius:5px;
                  display:inline-block;">
            Reset Password
        </a>
    </p>
    <p>If you did not request this, you can ignore this email.</p>
    """

    # 6️⃣ Create email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
    )

    # 7️⃣ Attach HTML
    email.attach_alternative(html_content, "text/html")

    # 8️⃣ Send email
    email.send()
