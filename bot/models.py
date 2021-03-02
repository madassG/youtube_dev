from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name="имя модели", max_length=40)


class User(models.Model):
    chat = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=40)
    target = models.TextField()
    youtube = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)


class Question(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_text = models.TextField()


class CompleteTask(models.Model):
    answer = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
