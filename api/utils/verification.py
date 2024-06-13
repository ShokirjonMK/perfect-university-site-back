from django.utils.crypto import get_random_string
from django.conf import settings
import sys

from api.utils.msg_sender import send_email

VERIFICATION_CODE_LENGTH = 6
DEFAULT_VERIFICATION_CODE = "081020"


def generate_session(length=16):
    return get_random_string(length=length)


def generate_verification_code():
    if settings.STAGE != "production" or "test" in sys.argv:
        return DEFAULT_VERIFICATION_CODE

    allowed_chars = "1234567890"
    return get_random_string(length=VERIFICATION_CODE_LENGTH, allowed_chars=allowed_chars)


def send_verification_code_via_email(email, code):
    if settings.STAGE == "production" and "test" not in sys.argv:
        subject = "Verification code"
        html_msg = f"Your verification code is {code}"
        send_email([email], subject, html_msg)


__all__ = ["generate_session", "generate_verification_code", "send_verification_code_via_email"]
