# Generated by Django 3.2.5 on 2022-01-10 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20220108_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
    ]
