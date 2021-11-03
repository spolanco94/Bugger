from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import MyUserCreationForm, MyUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name','is_staff', 'is_admin',
                    'is_active')
    list_filter = ('email', 'first_name', 'last_name', ' is_staff', 'is_admin',
                   'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 
                       'is_active')}
        ),
    )

admin.site.register(User, CustomUserAdmin)
