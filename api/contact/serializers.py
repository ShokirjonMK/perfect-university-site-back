from rest_framework import serializers
from admin_panel.model import contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.Contact
        fields = ["sender_name", "phone_number", "email", "message"]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact.UserEmail
        fields = ["email"]
