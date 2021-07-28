from django import forms
from django.forms import widgets

from .models import Project, Ticket

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

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'details', 'priority_level', 'attachments']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 80}),
            'attachments': widgets.ClearableFileInput(attrs={'multiple': True})
        }