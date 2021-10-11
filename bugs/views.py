from typing import ContextManager
from django.shortcuts import redirect, render

from .models import Comment, Project, Ticket
from .forms import CommentForm, ProjectForm, TicketForm

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
    comments = ticket.comment_set.order_by('date_added')
    
    # Comment system for tickets
    new_comment = None
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.ticket = ticket
            new_comment.save()
            return redirect(
                'bugs:ticket', 
                project_id=project.id, 
                ticket_id=ticket.id
                )

    context = {
        'ticket': ticket, 
        'project': project, 
        'comments': comments,
        'new_comment': new_comment,
        'form': form        
        }
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
        if form.is_valid():
            new_ticket = TicketForm(attachment=request.FILES['attachment'])
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
        form = TicketForm(instance=ticket, data=request.POST, file_field=request.FILES['attachment'])
        if form.is_valid():
            form.save()
            return redirect('bugs:ticket', project_id=project.id, ticket_id=ticket.id)
    
    context = {'project': project, 'ticket': ticket, 'form': form}
    return render(request, 'bugs/edit_ticket.html', context)

def edit_comment(request, prj_id, tkt_id, cmt_id):
    """Edit existing comment."""
    project = Project.objects.get(id=prj_id)
    ticket = Ticket.objects.get(id=tkt_id)
    comment = Comment.objects.get(id=cmt_id)

    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                            'bugs:ticket', 
                            ticket_id=ticket.id, 
                            project_id=project.id
                            )
        
    context = {
               'project': project, 
               'ticket': ticket, 
               'comment': comment, 
               'form': form
              }
    return render(request, 'bugs/edit_comment.html', context)
