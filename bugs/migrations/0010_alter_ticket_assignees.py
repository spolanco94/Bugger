# Generated by Django 3.2.5 on 2022-04-20 01:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bugs', '0009_ticket_assignees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assignees',
            field=models.ManyToManyField(blank=True, related_name='ticket_assignees', to=settings.AUTH_USER_MODEL),
        ),
    ]
