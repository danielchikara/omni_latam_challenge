# Generated by Django 3.2.8 on 2021-10-08 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_birth',
        ),
    ]
