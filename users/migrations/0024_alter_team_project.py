# Generated by Django 3.2.5 on 2022-01-11 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0002_auto_20211019_2253'),
        ('users', '0023_alter_user_assigned_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bugs.project'),
        ),
    ]
