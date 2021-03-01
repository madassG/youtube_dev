from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name="имя модели", max_length=40)


class User(models.Model):
    chat = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=40)
    target = models.TextField()
    youtube = models.URLField()

