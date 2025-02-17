from django.core.mail import send_mail
import random
from django.conf import settings
from .models import *

def send_otp_via_email(email):
    subject = f'your account verified'
    otp = random.randint(100000, 999999)
    message = f'your otp is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()