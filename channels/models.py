from django.db import models
from bot.models import User


class Channel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    videos_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.owner, self.created_at)
