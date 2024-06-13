from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS = (
    (0, _("Jarayonda")),
    (1, _("Ko'rildi")),
    (2, _("Rad etildi")),
)


class Contact(models.Model):
    sender_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact"
        ordering = ["-status"]

    def __str__(self):
        return str(self.sender_name)


class UserEmail(models.Model):
    email = models.EmailField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_email"

    def __str__(self):
        return str(self.email)
