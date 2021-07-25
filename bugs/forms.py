from django import forms
from django.forms import widgets

from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details']
        labels = {
            'title': '',
            'details': '',
            }
        widgets = {
            'details': forms.Textarea(attrs={'cols': 80}),
        }