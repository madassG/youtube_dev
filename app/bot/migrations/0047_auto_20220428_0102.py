# Generated by Django 3.1.4 on 2022-04-27 22:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0046_auto_20220428_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertime',
            name='time_from_last_message',
            field=models.TimeField(default=datetime.datetime(2022, 4, 28, 1, 2, 5, 123673)),
        ),
    ]