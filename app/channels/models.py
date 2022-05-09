from django.utils import timezone

from django.db import models
from bot.models import User
from users.models import Client, Reward


class Niche(models.Model):
    title = models.CharField(verbose_name="Название категории", max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Account(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Владелец', related_name='accounts')
    rewards = models.ManyToManyField(Reward, default=None, blank=True)

    purpose = models.TextField(blank=True, verbose_name="Цель")
    youtube = models.CharField(verbose_name="Идентификатор youtube канала", max_length=200)
    category = models.ForeignKey(Niche, on_delete=models.PROTECT, null=True, blank=True,
                                 verbose_name="Категория")

    playlist_id = models.CharField(max_length=200, blank=True, verbose_name="Плейлист youtube канала")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Заголовок канала")
    banner_url = models.CharField(max_length=600, blank=True, null=True, verbose_name="Аватарка канала")
    channel_country = models.CharField(max_length=600, blank=True, null=True, verbose_name="Страна канала")
    channel_keywords = models.TextField(blank=True, null=True, verbose_name="Указанные ключевые слова")

    subs_day = models.IntegerField(default=0, verbose_name="подписчики за день")
    subs_week = models.IntegerField(default=0, verbose_name="подписчики за неделю")
    subs_month = models.IntegerField(default=0, verbose_name="подписчики за месяц")
    subs_quarter = models.IntegerField(default=0, verbose_name="подписчики за квартал")

    views_day = models.IntegerField(default=0, verbose_name="просмотры за день")
    views_week = models.IntegerField(default=0, verbose_name="просмотры за неделю")
    views_month = models.IntegerField(default=0, verbose_name="просмотры за месяц")
    views_quarter = models.IntegerField(default=0, verbose_name="просмотры за квартал")

    is_username = models.BooleanField(default=False)
    rating = models.IntegerField(default=0, verbose_name="рейтинг")
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rating']
        verbose_name = "Канал пользователя"
        verbose_name_plural = "Канал пользователя"

    def __str__(self):
        return f"{self.owner} {self.youtube} {self.registration_date}"


class Channel(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Каналы', related_name='channels')
    subscribers = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    videos_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.owner, self.created_at)


class Video(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Видео', related_name='videos')
    url_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField()
    avatar = models.URLField(default='https://c0.klipartz.com/pngpicture/358/592/gratis-png-icono-de-signo-de-interrogacion-signo-de-interrogacion.png')
    title = models.CharField(blank=True, max_length=200)
    viewCount = models.IntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)
    commentsCount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner} {self.title}"
