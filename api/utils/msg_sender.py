from smtplib import SMTPAuthenticationError
import logging
from django.conf import settings
from django.core.mail import send_mail


def send_email(recipient_list: list, subject: str, message: str) -> None:
    email_from = settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, email_from, recipient_list)
    except SMTPAuthenticationError as e:
        logging.exception(e)
