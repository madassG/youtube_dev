# Generated by Django 3.1.4 on 2022-04-27 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20220428_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='rewards',
            field=models.ManyToManyField(default=None, to='users.Reward'),
        ),
    ]
