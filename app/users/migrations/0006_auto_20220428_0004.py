# Generated by Django 3.1.4 on 2022-04-27 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220428_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='special_color',
            field=models.CharField(default='#000', max_length=10),
        ),
    ]
