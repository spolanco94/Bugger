from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import MyUserCreationForm, MyUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name',)
    fieldsets = UserAdmin.fieldsets

admin.site.register(User, CustomUserAdmin)
