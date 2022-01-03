# Generated by Django 3.2.5 on 2022-01-02 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_team_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='team_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.team'),
            preserve_default=False,
        ),
    ]