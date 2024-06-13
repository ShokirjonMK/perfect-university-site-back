import os

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": os.environ.get("DB_NAME", "perfect"),
        "USER": os.environ.get("DB_USER", "user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        'ATOMIC_REQUESTS': True,
    }
}
HOST = "http://192.168.31.191:8080"
HR_HOST = "https://tsue-admin.wave.uz"

TOKEN = "5556550520:AAGMQLjOce_Jv6BK38yJZkGjNh3rCyQlsJM"
# group chat_id
CHAT_ID = "-1001482720952"
TEXT = "Янги ариза келиб тушди"

RECAPTCHA_PUBLIC_KEY = "6LdtyR0iAAAAAJ7rUZsGnM52_zYcIeoRCDLQIXDv"
RECAPTCHA_PRIVATE_KEY = "6LdtyR0iAAAAAFoD69lODqv5Figk00g_jF1A4cJQ"

DEBUG = True

INTERNAL_IPS = [
    "127.0.0.1",
]
