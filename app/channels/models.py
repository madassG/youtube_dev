from django.db import models
from bot.models import User


class Channel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Каналы', related_name='channels')
    subscribers = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    videos_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.owner, self.created_at)


class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Видео', related_name='videos')
    url_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField()
    avatar = models.URLField(default='https://c0.klipartz.com/pngpicture/358/592/gratis-png-icono-de-signo-de-interrogacion-signo-de-interrogacion.png')
    title = models.CharField(blank=True, max_length=200)
    viewCount = models.IntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)
    commentsCount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner} {self.title}"
