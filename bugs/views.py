from django.shortcuts import redirect, render

from .models import Project, Ticket
from .forms import ProjectForm

def index(request):
    """The home page for Bugger"""
    return render(request, 'bugs/index.html')

def projects(request):
    """Page displaying all projects by date added."""
    projects = Project.objects.order_by('date_added')
    context = {'projects': projects}
    return render(request, 'bugs/projects.html', context)

def project(request, project_id):
    """Page displaying details and tickets of a project."""
    project = Project.objects.get(id=project_id)
    tickets = project.ticket_set.order_by('date_added')
    context = {'project': project, 'tickets': tickets}
    return render(request, 'bugs/project.html', context)

def ticket(request, project_id, ticket_id):
    """Page displaying details of a ticket."""
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)
    context = {'ticket': ticket, 'project': project}
    return render(request, 'bugs/ticket.html', context)

def new_project(request):
    """Create a new project."""
    if request.method != "POST":
        # No data submitted, create a blank form
        form = ProjectForm
    else:
        form = ProjectForm(data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('bugs:projects')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'bugs/new_project.html', context)
