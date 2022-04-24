from django.contrib.auth.forms import UserCreationForm
from authApp.models import CustomUser, Profile
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('user',)
