# Generated by Django 3.2.5 on 2021-07-16 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0002_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='attachments',
            field=models.FileField(blank=True, null=True, upload_to='attachments/%Y/%m/%d'),
        ),
    ]
