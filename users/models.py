from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db.models.base import Model
from django.core.mail import send_mail
from django.conf import settings

from bugs.models import Project
from django.conf import settings

class Team(models.Model):
    """
        Defines Team model where each user will only be able to belong to 
        one team at any given time.
    """
    name = models.CharField(max_length=125, unique=True)
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name="managed_team", 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.TextField(max_length=1024)
    project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
        Defines a custom User class where the user's email will serve as their
        username, and their role will be assigned from a predetermined set of
        options.
    """
    ROLE_CHOICES = [
        (1, 'Administrator'),
        (2, 'Project Manager'),
        (3, 'Developer'),
        (4, 'Designer'),
    ]
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first name', 
        max_length=50,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='last name', 
        max_length=50,
        blank=True
    )
    role = models.IntegerField(choices=ROLE_CHOICES)
    assigned_team = models.ForeignKey(
        Team, 
        on_delete=models.SET_NULL, 
        related_name='members',
        null=True, 
        blank=True,
    )
    date_joined = models.DateTimeField(
        verbose_name='date joined',
        auto_now_add=True,
    )
    is_administrator = models.BooleanField(default=False)
    is_project_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def get_full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.rstrip()
    
    def get_short_name(self) -> str:
        return self.first_name

    def email_user(self, subject: str, message: str, from_email: str = ..., 
                   **kwargs: str) -> None:
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_role_choices(self, new_role: str):
        self.ROLE_CHOICES.append((len(ROLE_CHOICES), new_role.capitalize()))
    
    def update_team(self, team):
        if team == None:
            self.assigned_team = None
        self.assigned_team = team

    def __str__(self):
        return self.email

    objects = UserManager()
