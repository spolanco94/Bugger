# Generated by Django 3.2.5 on 2021-07-14 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('details', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
