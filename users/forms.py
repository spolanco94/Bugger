from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')
