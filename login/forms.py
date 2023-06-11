from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import EmailField

class CustomUserCreationForm(UserCreationForm):
    email = EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email Already Exists')

        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        fields_classes = {'username': UsernameField}
