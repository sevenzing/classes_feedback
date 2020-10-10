from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class PTDLoginForm(forms.Form):
    email = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="", help_text="", widget=forms.PasswordInput({'placeholder': 'Password'}))


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'surname')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email','name', 'surname')
