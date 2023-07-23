from django import forms
from django.contrib.auth.forms import UserCreationForm


# The default registration form should suffice for registering new accounts in this environment
class RegistrationForm(UserCreationForm):
    pass