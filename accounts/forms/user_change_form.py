from django import forms
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'avatar']