from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from .models import Client


class ClientCreationForm(UserCreationForm):

    class Meta:
        model = Client
        fields = ('email', 'password')


class ClientChangeForm(UserChangeForm):

    class Meta:
        model = Client
        fields = ('name',
                  'surname',
                  'age',
                  'phone',
                  'email',
                  'email_proved',
                  'telegram_chat',
                  'subscription',
                  'rewards',
                  'password',
                  )
