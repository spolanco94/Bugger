from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import Http404

from .models import User
from .forms import MyUserCreationForm, MyUserChangeForm

def check_user(request, user_obj):
    """Checks if the requesting user is the owner of the object in question."""
    if user_obj != request.user:
        raise Http404

def register(request):
    """User registration form."""

    if request.method != 'POST':
        form = MyUserCreationForm()
    else:
        form = MyUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)

            new_user.is_active = False
            if new_user.role == 1:
                new_user.is_administrator = True
                new_user.is_superuser = True  
                new_user.is_staff = True
            elif new_user.role == 2:
                new_user.is_project_manager = True
            elif new_user.role == 3:
                new_user.is_developer = True
            elif new_user.role == 4:
                new_user.is_designer = True

            new_user.save()

            # log in new user
            login(request, new_user)
            return redirect('bugs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def profile(request, user_id):
    """Displays user profile with account information."""
    user = User.objects.get(id=user_id)
    check_user(request, user)

    if request.method != 'POST':
        form = MyUserChangeForm(instance=user)
    else:
        form = MyUserChangeForm(instance=user, data=request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('users:profile', user_id=user.id)        

    context = {'user': user, 'form': form}
    return render(request, 'registration/profile.html', context)
