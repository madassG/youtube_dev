# Generated by Django 3.1.4 on 2022-04-27 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_client_rewards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='subscription',
        ),
    ]
