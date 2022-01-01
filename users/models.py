from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db.models.base import Model
from django.core.mail import send_mail

class User(AbstractUser):
    ROLE_CHOICES = (
        (1, 'Administrator'),
        (2, 'Project Manager'),
        (3, 'Developer'),
        (4, 'Basic'),
    )

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
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(
        verbose_name='date joined',
        auto_now_add=True,
    )
    is_administrator = models.BooleanField(default=False)
    is_project_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_basic_user = models.BooleanField(default=False)

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

    def __str__(self):
        return self.email

    objects = UserManager()
