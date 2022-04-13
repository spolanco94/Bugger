from django import forms
from django.db import models
from django.forms import widgets
from django.db.models import Q

from .models import Comment, Project, Ticket, Files
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
        fields = ['title', 'details', 'priority_level',]
        widgets = {
            'details': forms.Textarea(attrs={'cols': 80}),
            # 'attachments': widgets.ClearableFileInput(attrs={'multiple': True})
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['img']
        widgets = {
            'img': widgets.ClearableFileInput(attrs={'multiple': True}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 60}),
        }

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.get_full_name()} | {obj.email}"

class TeamCreationForm(forms.ModelForm):

    name = forms.CharField()   
    manager = forms.ModelChoiceField(
        queryset = User.objects.all(), 
        empty_label=None,
    )
    project = forms.ModelChoiceField(
        queryset = Project.objects.all(),
        required=False
    )

    members = CustomMMCF(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = ['name', 'manager', 'project', 'members', 'description',]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5})
        }
