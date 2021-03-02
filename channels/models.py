from django.db import models
from bot.models import User

# Create your models here.


class Channels(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    videos_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
