# forms.py in your members app

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']
