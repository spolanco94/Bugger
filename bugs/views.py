from msilib.schema import File
from operator import indexOf
import os
from typing import ContextManager
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from django.core.files.storage import default_storage

from .models import Comment, Project, Ticket, Files
from .forms import CommentForm, ProjectForm, TicketForm, FileForm, TeamCreationForm, StatusForm, AssignTicketForm

from users.models import Team, User

def check_owner(request, obj):
    """Checks if the requesting user is the owner of the object in question."""
    if obj.owner != request.user:
        raise Http404

def check_admin_or_manager(request):
    """Checks if the requesting user is an administrator or a project manager."""
    if not request.user.is_administrator and not request.user.is_project_manager:
        return False
    return True

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
    files = ticket.files_set.order_by('name')
    print(ticket.assignees.all())
    # for file in files:
    #     print(file.img.url)
        # try:
        #     default_storage.exists(os.path.join(file.img.url))
        # except IOError:
        #     files.remove(file)

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
        'files': files,
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
        ticket_form = TicketForm()
        file_form = FileForm()
    else:
        ticket_form = TicketForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        files = request.FILES.getlist('img')
        if ticket_form.is_valid() and file_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.project = project
            new_ticket.owner = request.user
            new_ticket.status = 'S'
            new_ticket.save()
            
            # Attach files
            for count, f in enumerate(files, 1):
                file_instance = Files(name=f'attachment_{count}', img=f)
                file_instance.save()
            new_files = file_form.save(commit=False)
            new_files.ticket = new_ticket
            new_files.save()

            return redirect('bugs:ticket', project_id=project.id, ticket_id=new_ticket.id)

    context = {
        'project': project, 
        'ticket_form': ticket_form, 
        'file_form': file_form
    }
    return render(request, 'bugs/new_ticket.html', context)

@login_required
def edit_ticket(request, project_id, ticket_id):
    """Edit an exisiting ticket."""
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)
    # files = Files.objects.get(ticket=ticket)
    check_owner(request, ticket)

    if request.method != 'POST':
        # Prefill form with data from database
        ticket_form = TicketForm(instance=ticket)
        # for file in files:
        #     file_form = FileForm(instance=file)
    else:
        ticket_form = TicketForm(instance=ticket, data=request.POST)
        # file_form = FileForm(instance=file, data=request.POST, files=request.FILES)
        # files = request.FILES.getlist('img')
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.save()
            
            # for count, f in enumerate(files, 1):
            #     file_instance = Files(name=f'attachment_{count}', img=f, ticket=ticket)
            #     file_instance.save()
            # file_form.save()
            
            return redirect('bugs:ticket', project_id=project.id, ticket_id=ticket.id)
    
    context = {
        'project': project, 
        'ticket': ticket, 
        'ticket_form': ticket_form, 
        # 'file_form': file_form
    }
    return render(request, 'bugs/edit_ticket.html', context)

@login_required
def update_ticket_status(request, project_id, ticket_id):
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)
    check_admin_or_manager(request)

    if request.method != 'POST':
        # Prefill form with data from database
        form = StatusForm(instance=ticket)
    else:
        form = StatusForm(instance=ticket, data=request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            
            return redirect('bugs:ticket', project_id=project.id, ticket_id=ticket.id)
    
    context = {
        'project': project, 
        'ticket': ticket, 
        'form': form,
    }
    return render(request, 'bugs/update_ticket_status.html', context)

@login_required
def assign_ticket(request, project_id, ticket_id):
    project = Project.objects.get(id=project_id)
    ticket = Ticket.objects.get(id=ticket_id)
    check_admin_or_manager(request)

    if request.method != 'POST':
        # Prefill form with data from database
        form = AssignTicketForm(instance=ticket)
    else:
        form = AssignTicketForm(instance=ticket, data=request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            
            assignees = form.cleaned_data['assignees']
            for user in assignees:
                ticket.assign_ticket(user)
                ticket.save()
                user.save()

            ticket.save()
            
            return redirect('bugs:ticket', project_id=project.id, ticket_id=ticket.id)
    
    context = {
        'project': project, 
        'ticket': ticket, 
        'form': form,
    }
    return render(request, 'bugs/assign_ticket.html', context)

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
    # Check if requesting user is an admin or manager
    if not check_admin_or_manager(request):
        # print(f'user: {request.user.assigned_team.id}')
        # If not, check if they are assigned to a team.
        # If they are, direct them to that teams' page. Otherwise raise Http404 error
        if request.user.assigned_team:
            return team(request, request.user.assigned_team.id)
        
        raise Http404
    
    teams = Team.objects.order_by('date_created')
    context = {'teams': teams}
    return render(request, 'bugs/teams.html', context)

@login_required
def new_team(request):
    """Form page to create a new team."""
    check_admin_or_manager(request)

    if request.method != "POST":
        # No data submitted, create a blank form
        form = TeamCreationForm()
        
        # Filter selectable members to those without an assigned team.
        members = form.fields['members']
        members.queryset = User.objects.filter(assigned_team=None)
        
        # Filter selectable managers to those without a team and are either 
        # administrator or project manager status.
        manager = form.fields['manager']
        manager.queryset = User.objects.filter(
            Q(managed_team=None) & 
            (Q(is_administrator=True) | Q(is_project_manager=True))
        )

        # Filter projects to those without a team assigned. 
        # (May be changed so that projects can have multiple teams assigned.)
        project = form.fields['project']
        project.queryset = Project.objects.filter(team=None)
        
    else:
        form = TeamCreationForm(data=request.POST)
        if form.is_valid():
            new_team = form.save(commit=False)

            # Assign team to manager
            manager = form.cleaned_data['manager']
            manager.update_team(new_team)
            new_team.save()
            manager.save()

            # Assign the team to each of the remaining members
            members = form.cleaned_data['members']
            for member in members:
                member.update_team(new_team)
                new_team.save()
                member.save()
            
            return redirect('bugs:teams')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'bugs/new_team.html', context)

@login_required
def team(request, team_id):
    """Displays information about a specific team."""
    team = Team.objects.get(id=team_id)
    
    context = {'team': team}
    return render(request, 'bugs/team.html', context)

@login_required
def edit_team(request, team_id):
    """Edit existing comment."""
    team = Team.objects.get(id=team_id)

    if not request.user.is_administrator and request.user != team.manager:
        raise Http404

    if request.method != 'POST':
        form = TeamCreationForm(instance=team)
        form.fields['members'].initial = (
            User.objects.filter(assigned_team=team)
        )
    else:
        form = TeamCreationForm(instance=team, data=request.POST)
        if form.is_valid():
            team = form.save(commit=False)

            # Assign team to manager
            manager = form.cleaned_data['manager']
            manager.update_team(team)
            team.save()
            manager.save()

            # Assign the team to each of the remaining members
            members = form.cleaned_data['members']
            for curr_member in team.members.all():
                if curr_member not in members:
                    curr_member.update_team(None)
                    print(curr_member)
                    team.save()
                    curr_member.save()
            for member in members:
                member.update_team(team)
                team.save()
                member.save()
                
            return redirect('bugs:team', team_id=team.id)

    context = {'team': team, 'form': form}
    return render(request, 'bugs/edit_team.html', context)
