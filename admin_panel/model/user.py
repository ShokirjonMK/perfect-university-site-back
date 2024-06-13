from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rolepermissions.roles import assign_role


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="custom_user")
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.FileField(upload_to="user", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_custom(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            assign_role(instance, "admin")
        elif instance.is_staff:
            assign_role(instance, "staff")
        else:
            assign_role(instance, "regular_user")
