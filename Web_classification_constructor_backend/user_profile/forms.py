from django import forms


class UserProfileForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'required': True}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'required': True}))
