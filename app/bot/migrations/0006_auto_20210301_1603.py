# Generated by Django 3.1.7 on 2021-03-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_remove_user_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chat',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]