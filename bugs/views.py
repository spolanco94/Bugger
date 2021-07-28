from typing import ContextManager
from django.shortcuts import redirect, render

from .models import Project, Ticket
from .forms import ProjectForm, TicketForm

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
        form = ProjectForm()
    else:
        form = ProjectForm(data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('bugs:projects')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'bugs/new_project.html', context)

def edit_project(request, project_id):
    """Edit a current project."""
    project = Project.objects.get(id=project_id)

    if request.method != 'POST':
        # Generate form prefilled with current data
        form = ProjectForm(instance=project)
    else:
        # Update existing entry with new information
        form = ProjectForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bugs:project', project_id=project.id)

    # Display invalid form
    context = {'project': project, 'form': form}
    return render(request, 'bugs/edit_project.html', context)

def new_ticket(request, project_id):
    """Create a new ticket for a project."""
    project = Project.objects.get(id=project_id)

    if request.method != 'POST':
        form = TicketForm()
    else:
        form = TicketForm(request.POST, request.FILES)
        files = request.FILES.getlist('attachments')
        if form.is_valid():
            for f in files:
                print(f)
                file_instance = Ticket(attachments=f)
                file_instance.save()
            new_ticket = form.save(commit=False)
            new_ticket.project = project
            new_ticket.save()
            return redirect('bugs:project', project_id=project.id)

    context = {'project': project, 'form': form}
    return render(request, 'bugs/new_ticket.html', context)

def edit_ticket(request, project_id, ticket_id):
    """Edit an exisiting ticket."""
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method != 'POST':
        # Prefill form with data from database
        form = TicketForm(instance=ticket)
    else:
        form = TicketForm(instance=ticket, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bugs:project', project_id=project.id)
    
    context = {'project': project, 'ticket': ticket, 'form': form}
    return render(request, 'bugs/edit_ticket.html', context)
