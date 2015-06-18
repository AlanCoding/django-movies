from django import forms
from django.contrib.auth.models import User
from Rater.models import Rater, Rating
# Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class RaterForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ('age', 'gender', 'occupation', 'zip_code',)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating', 'review',)

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
