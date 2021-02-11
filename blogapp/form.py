from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from simplemathcaptcha.fields import MathCaptchaField
from .models import Blog

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    captcha = MathCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]


