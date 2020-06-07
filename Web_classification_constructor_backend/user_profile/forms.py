from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'password',
        )
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'password': forms.PasswordInput(attrs={'required': True}),
        }
