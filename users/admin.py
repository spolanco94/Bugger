from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import User, Team
from .forms import MyUserCreationForm, MyUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    readonly_fields=('date_joined',)
    form = MyUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'team_group', 'date_joined',
                    'is_administrator', 'is_project_manager', 'is_developer', 
                    'is_designer')
    fieldsets = (
        (   
            'Personal Info',
            {
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'date_joined',
                ),
            },
        ),
        (   
            'Default Info',
            {
                'fields': (
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'groups',
                ),
            },
        ),
        (
            'Roles and Permissions',
            {
                'fields': (
                    'role',
                    'team_group',
                    'is_administrator',
                    'is_project_manager', 
                    'is_developer', 
                    'is_designer',
                ),
            },
        ),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Team)
