from django.shortcuts import render, redirect
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm

from .models import User
from .forms import MyUserCreationForm, MyUserChangeForm

def register(request):
    """User registration form."""

    if request.method != 'POST':
        form = MyUserCreationForm()
    else:
        form = MyUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()

            # log in new user
            login(request, new_user)
            return redirect('bugs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)
