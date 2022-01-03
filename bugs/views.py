from typing import ContextManager
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Comment, Project, Ticket
from .forms import CommentForm, ProjectForm, TicketForm
from users.models import Team

def check_owner(request, obj):
    """Checks if the requesting user is the owner of the object in question."""
    if obj.owner != request.user:
        raise Http404

def index(request):
    """The home page for Bugger"""
    return render(request, 'bugs/index.html')

@login_required
def projects(request):
    """Page displaying all projects by date added."""
    projects = Project.objects.order_by('date_added')
    context = {'projects': projects}
    return render(request, 'bugs/projects.html', context)

@login_required
def project(request, project_id):
    """Page displaying details and tickets of a project."""
    project = Project.objects.get(id=project_id)
    tickets = project.ticket_set.order_by('date_added')
    context = {'project': project, 'tickets': tickets}
    return render(request, 'bugs/project.html', context)

@login_required
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
            new_comment.owner = request.user
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

@login_required
def new_project(request):
    """Create a new project."""
    if request.method != "POST":
        # No data submitted, create a blank form
        form = ProjectForm()
    else:
        form = ProjectForm(data=request.POST)
        if form.is_valid:
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            return redirect('bugs:projects')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'bugs/new_project.html', context)

@login_required
def edit_project(request, project_id):
    """Edit a current project."""
    project = Project.objects.get(id=project_id)
    check_owner(request, project)

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

@login_required
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
                file_instance = Ticket(attachments=f)
                file_instance.save()
            new_ticket = form.save(commit=False)
            new_ticket.project = project
            new_ticket.owner = request.user
            new_ticket.save()
            return redirect('bugs:project', project_id=project.id)

    context = {'project': project, 'form': form}
    return render(request, 'bugs/new_ticket.html', context)

@login_required
def edit_ticket(request, project_id, ticket_id):
    """Edit an exisiting ticket."""
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)
    check_owner(request, ticket)

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

@login_required
def edit_comment(request, prj_id, tkt_id, cmt_id):
    """Edit existing comment."""
    project = Project.objects.get(id=prj_id)
    ticket = Ticket.objects.get(id=tkt_id)
    comment = Comment.objects.get(id=cmt_id)
    check_owner(request, comment)

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

@login_required
def teams(request):
    """Page displaying all teams and their respective manager(s)."""
    if not request.user.is_administrator and not request.user.is_project_manager:
        raise Http404
    teams = Team.objects.order_by('date_created')
    context = {'teams': teams}
    return render(request, 'bugs/teams.html', context)
