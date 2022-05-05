# Generated by Django 3.1.7 on 2021-03-10 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_auto_20210309_1852'),
        ('channels', '0004_auto_20210310_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='bot.user', verbose_name='Каналы'),
        ),
        migrations.AlterField(
            model_name='video',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='bot.user', verbose_name='Видео'),
        ),
    ]