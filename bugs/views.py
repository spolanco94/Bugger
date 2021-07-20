from django.shortcuts import render

from .models import Project

def index(request):
    """The home page for Bugger"""
    return render(request, 'bugs/index.html')

def projects(request):
    """Page displaying all projects by date added."""
    projects = Project.objects.order_by('date_added')
    context = {'projects': projects}
    return render(request, 'bugs/projects.html', context)
