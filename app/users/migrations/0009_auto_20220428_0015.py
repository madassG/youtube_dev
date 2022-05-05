# Generated by Django 3.1.4 on 2022-04-27 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220428_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='belonging',
            field=models.IntegerField(choices=[(1, 'Канал'), (2, 'Пользователь')]),
        ),
        migrations.AlterField(
            model_name='reward',
            name='image',
            field=models.ImageField(help_text='Квадратное изображение. Оптимальный размер - 256x256', upload_to=''),
        ),
        migrations.AlterField(
            model_name='reward',
            name='type',
            field=models.IntegerField(choices=[(1, 'Период'), (2, 'Просмотры'), (3, 'Подписчики'), (4, 'Количество видео'), (5, 'Специальное')]),
        ),
    ]
