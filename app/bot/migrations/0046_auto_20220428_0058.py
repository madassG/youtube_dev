# Generated by Django 3.1.4 on 2022-04-27 21:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0045_auto_20220428_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertime',
            name='time_from_last_message',
            field=models.TimeField(default=datetime.datetime(2022, 4, 28, 0, 58, 6, 398277)),
        ),
    ]
