# Generated by Django 3.1.7 on 2021-03-11 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0006_auto_20210311_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
