# Generated by Django 3.1.4 on 2022-04-26 20:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0028_auto_20220426_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertime',
            name='time_from_last_message',
            field=models.TimeField(default=datetime.datetime(2022, 4, 26, 23, 3, 42, 327006)),
        ),
    ]