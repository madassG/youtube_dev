from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name="имя модели", max_length=40)

    def __str__(self):
        return self.name


class User(models.Model):
    chat = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=40)
    target = models.TextField()
    youtube = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    playlist_id = models.CharField(max_length=200, blank=True)
    is_username = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.name} {self.chat}'


class Question(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    task_rating = models.IntegerField(default=2)

    def __str__(self):
        return self.question


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_text = models.TextField()

    def __str__(self):
        return self.task_name


class CompleteTask(models.Model):
    class StatusTask(models.TextChoices):
        CHECK = 'CH', 'Задание на проверке'
        COMPLETE = 'CM', 'Задание выполнено'
        FAIL = 'FL', 'Задание провалено'

    answer = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=2, choices=StatusTask.choices, default=StatusTask.CHECK)
    comment = models.TextField(default="")

    def __str__(self):
        return f'{self.task} {self.user}'
