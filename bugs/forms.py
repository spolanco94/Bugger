from django import forms
from django.db import models
from django.forms import widgets
from django.db.models import Q

from .models import Comment, Project, Ticket
from users.models import User, Team

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 60}),
        }

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'manager', 'description',]
        
        name = forms.CharField()
        manager = forms.ModelMultipleChoiceField(
            queryset = User.objects.filter(
                Q(role=1) &
                Q(role=2)
            )
        )
        # widgets = {
        #     'name': forms.CharField(attrs={'is_hidden':False}),
        #     'manager': forms.ModelMultipleChoiceField(
        #         queryset=User.objects.filter()
        #     )
        # }
