from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    phone_number = PhoneNumberField(max_length=12, unique=True, null=False)
    authentication_code = models.CharField(max_length=4, null=False)
    invite_code = models.CharField(max_length=6, null=False)
    access_token = models.CharField(max_length=245)
    used_code = models.CharField(max_length=6, null=True)
