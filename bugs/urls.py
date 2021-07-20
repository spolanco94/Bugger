"""Define URL patterns for bugs app."""

from django.urls import path

from . import views

app_name = 'bugs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Projects page
    path('projects/', views.projects, name='projects'),
]
