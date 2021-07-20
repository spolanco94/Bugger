from django.db import models
from django.db.models.fields import CharField, TextField
from django.db.models.fields.related import ForeignKey

class Project(models.Model):
    """A project currently being tracked."""
    title = models.CharField(max_length=150)
    details = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

class Ticket(models.Model):
    """Define ticket specific to a project."""
    PRIORITY_LEVEL_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]
    
    project = ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    details = models.TextField()
    priority_level = models.CharField(
        max_length=1, 
        choices=PRIORITY_LEVEL_CHOICES,
        default='M',
    )
    date_added = models.DateTimeField(auto_now_add=True)
    attachments = models.FileField(
        upload_to='attachments/%Y/%m/%d', 
        blank=True, 
        null=True
    )

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    """A comment made by a user directly on a ticket."""
    ticket = ForeignKey(Ticket, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if len(self.comment) > 50:
            return f"{self.comment[:50]}..."
        
        return self.comment
