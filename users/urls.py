from django import urls
from django.urls import path
from django.urls.conf import include

from . import views

app_name = 'users'
urlpatterns = [
    # Login page
    path('', include('django.contrib.auth.urls')),
]
