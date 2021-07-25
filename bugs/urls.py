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
]
