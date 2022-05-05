# Generated by Django 3.1.4 on 2022-04-27 21:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20220428_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='created_at',
        ),
        migrations.AddField(
            model_name='client',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]