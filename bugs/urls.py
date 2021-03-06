"""Define URL patterns for bugs app."""

from django.urls import path

from . import views

app_name = 'bugs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Projects page
    path('projects/', views.projects, name='projects'),
    # Project page
    path('projects/<int:project_id>', views.project, name='project'),
    # Ticket page
    path(
        'projects/<int:project_id>/tickets/<int:ticket_id>', 
        views.ticket, 
        name='ticket'
        ),
    # New project page
    path('new_project/', views.new_project, name='new_project'),
    # Edit project page
    path(
        'edit_project/<int:project_id>', 
        views.edit_project, 
        name='edit_project'
        ),
    # New ticket page
    path(
        'projects/<int:project_id>/new_ticket/', 
        views.new_ticket, 
        name='new_ticket'
        ),
    # Edit ticket page
    path(
        'projects/<int:project_id>/tickets/<int:ticket_id>/edit_ticket/', 
        views.edit_ticket, 
        name='edit_ticket'
        ),
    # Update ticket status page
    path(
        'projects/<int:project_id>/tickets/<int:ticket_id>/ticket_status_update/', 
        views.update_ticket_status, 
        name='update_ticket_status'
        ),
    # Assign ticket to a user
    path(
        'projects/<int:project_id>/tickets/<int:ticket_id>/assign_ticket/', 
        views.assign_ticket, 
        name='assign_ticket'
        ),
    # Edit comment page
    path(
        'projects/<int:prj_id>/tickets/<int:tkt_id>/<int:cmt_id>/edit_comment/', 
        views.edit_comment, 
        name='edit_comment'
        ),
    # Teams directory page
    path('teams/', views.teams, name='teams'),
    # New team page
    path('new_team/', views.new_team, name='new_team'),
    # Team page
    path('teams/<int:team_id>', views.team, name='team'),
    # Team page
    path('teams/<int:team_id>/edit_team', views.edit_team, name='edit_team'),
]
