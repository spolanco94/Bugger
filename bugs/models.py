from django.contrib.auth import login
from django.db import models
from django.db.models.fields import CharField, TextField
from django.db.models.fields.related import ForeignKey
from django.conf import settings

class Project(models.Model):
    """A project currently being tracked."""
    title = models.CharField(max_length=150)
    details = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title

class Ticket(models.Model):
    """Define ticket specific to a project."""
    PRIORITY_LEVEL_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('S', 'Submitted'),
        ('R', 'In Review'),
        ('A', 'Assigned'),
        ('C', 'Closed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    details = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='ticket_owner')
    priority_level = models.CharField(
        max_length=1, 
        choices=PRIORITY_LEVEL_CHOICES,
        default='M',
    )
    status = models.CharField(
        max_length=1, 
        choices=STATUS_CHOICES,
        default='S',
    )
    assignees = models.ManyToManyField(
        "users.User", 
        related_name='ticket_assignees',
        blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    # attachments = models.FileField(
    #     upload_to='attachments/%Y/%m/%d', 
    #     blank=True, 
    #     null=True
    # )

    class Meta:
        verbose_name_plural = 'tickets'

    def __str__(self) -> str:
        return self.title

    def assign_ticket(self, user):
        if user == None:
            return
        user.ticket_assignees.add(self)

class Comment(models.Model):
    """A comment made by a user directly on a ticket."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if len(self.comment) > 50:
            return f"{self.comment[:50]}..."
        
        return self.comment

class Files(models.Model):
    name = models.CharField(max_length=150)
    img = models.FileField(
        upload_to='attachments/%Y/%m/%d', 
        null=True, 
        blank=True
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
