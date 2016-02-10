from django.utils.translation import ugettext as _
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=40)
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput())
