# Generated by Django 3.1.7 on 2021-03-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0016_task_is_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='completetask',
            name='okey',
            field=models.BooleanField(default=False),
        ),
    ]
