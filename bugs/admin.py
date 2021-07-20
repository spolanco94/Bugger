from django.contrib import admin

from .models import Comment, Project, Ticket

admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(Comment)