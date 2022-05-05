# Generated by Django 3.1.4 on 2022-05-01 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0010_auto_20220428_0128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='target',
        ),
        migrations.AddField(
            model_name='account',
            name='purpose',
            field=models.TextField(blank=True, verbose_name='Цель'),
        ),
        migrations.AlterField(
            model_name='account',
            name='playlist_id',
            field=models.CharField(blank=True, max_length=200, verbose_name='Плейлист youtube канала'),
        ),
    ]
