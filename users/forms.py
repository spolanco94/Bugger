from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

class MyUserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        # Set disabled fields
        self.fields['role'].disabled = True
        self.fields['assigned_team'].disabled = True
        # self.fields['date_joined'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'assigned_team')
