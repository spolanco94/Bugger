from django import urls
from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

app_name = 'users'
urlpatterns = [
    # Registration page
    path('register/', views.register, name='register'),
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),
    # Password Reset Done
    path('password_reset/', auth_views.PasswordResetDoneView.as_view(), 
        name='password_reset_done'),
    # Password Reset Confirm
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),
    # Password Reset Complete
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), 
        name='password_reset_complete'),
    # Default authentication URL's
    path('', include('django.contrib.auth.urls')),
]
