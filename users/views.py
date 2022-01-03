from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import User
from .forms import MyUserCreationForm, MyUserChangeForm

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
