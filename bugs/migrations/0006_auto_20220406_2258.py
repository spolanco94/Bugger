# Generated by Django 3.2.5 on 2022-04-07 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0005_alter_files_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='files',
            options={},
        ),
        migrations.RenameField(
            model_name='files',
            old_name='file',
            new_name='img',
        ),
    ]