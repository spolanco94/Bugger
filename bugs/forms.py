from django import forms
from django.db import models
from django.forms import widgets

from .models import Comment, Project, Ticket

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
        fields = ['title', 'details', 'priority_level', 'attachment']
        widgets = {
            'details': forms.Textarea(attrs={'cols': 80}),
            'attachment': widgets.ClearableFileInput(attrs={'multiple': True})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 60}),
        }
