from django.core.mail import send_mail as django_send_mail
from django.conf import settings

def send_mail(msg,to):
    subject = "TradeSquare"
    message = msg
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to]
    django_send_mail(subject, message, from_email, recipient_list)