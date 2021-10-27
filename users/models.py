from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db.models.base import Model
from django.core.mail import send_mail

class Roles(models.Model):
    """User roles"""
    ADMIN = 1
    MANAGER = 2
    DEVELOPER = 3
    USER = 4
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MANAGER, 'manager'),
        (DEVELOPER, 'developer'),
        (USER, 'user'),
    )

    id = models.PositiveSmallIntegerField(
                                          choices=ROLE_CHOICES, 
                                          primary_key=True,
                                          )

    def __str__(self) -> str:
        return self.get_id_display()

class User(AbstractUser):
    roles = models.ManyToManyField(Roles)
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
    date_joined = models.DateTimeField(
        verbose_name='date joined',
        auto_now_add=True,
    )

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
