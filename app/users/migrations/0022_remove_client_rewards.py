# Generated by Django 3.1.4 on 2022-04-27 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20220428_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='rewards',
        ),
    ]