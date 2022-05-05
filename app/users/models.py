from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class Reward(models.Model):
    belonging = models.IntegerField(
        choices=(
            (1, 'Канал'),
            (2, 'Пользователь'),
        )
    )

    type = models.IntegerField(
        choices=(
            (1, 'Период'),
            (2, 'Просмотры'),
            (3, 'Подписчики'),
            (4, 'Количество видео'),
            (5, 'Специальное')
        )
    )

    amount = models.CharField(max_length=100)
    image = models.ImageField(help_text='Квадратное изображение. Оптимальный размер - 256x256', upload_to='rewards/')

    def __str__(self):
        belonging = {
            1: 'Для канала',
            2: 'Для пользователя'
        }

        reward_type = {
            1: 'по периоду',
            2: 'по просмотрам',
            3: 'по подписчикам',
            4: 'по количеству видео',
            5: 'специальная'
        }

        return f'{belonging[self.belonging]} {reward_type[self.type]} - {self.amount}'


class Subscription(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    desc = models.TextField(max_length=500, blank=True, null=True)

    max_channels = models.IntegerField(default=1)
    check_frequency = models.IntegerField(default=1)
    check_time = models.IntegerField(default=7)
    check_frequency_after_check_time = models.IntegerField(default=7)
    check_time_2 = models.IntegerField(default=28)
    special_color = models.CharField(default='#000', max_length=10)

    def __str__(self):
        return f'{self.title} {self.max_channels}.{self.check_frequency}.{self.check_time}.\
{self.check_frequency_after_check_time}.{self.check_time_2}'


class Client(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    phone = models.IntegerField(unique=True)
    email = models.EmailField(verbose_name='Адрес электронной почты', max_length=255, unique=True)
    email_proved = models.BooleanField(default=False)
    telegram_chat = models.IntegerField(default=-1)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    rewards = models.ManyToManyField(Reward, default=None, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_check = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return f'{self.surname} {self.name}'

    def get_short_name(self):
        return self.name

    def get_phone(self):
        return self.phone
