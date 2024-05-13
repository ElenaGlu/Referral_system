from django import forms
from django.forms import CharField
from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    phone_number = PhoneNumberField(max_length=12)


class AuthenticationForm(forms.Form):
    authentication_code = CharField(max_length=4)


class InviteForm(forms.Form):
    invite_code = CharField(max_length=6)
