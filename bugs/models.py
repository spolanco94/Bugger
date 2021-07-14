from django.db import models
from django.db.models.fields import CharField, TextField

class Project(models.Model):
    """Define project models."""
    title = models.CharField(max_length=150)
    details = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
