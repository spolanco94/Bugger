# Generated by Django 3.2.5 on 2022-01-11 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0002_auto_20211019_2253'),
        ('users', '0024_alter_team_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='manager',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bugs.project'),
        ),
        migrations.AlterField(
            model_name='user',
            name='assigned_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='users.team'),
        ),
    ]
