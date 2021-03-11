from django.db import models
from datetime import date
# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name="имя модели", max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class User(models.Model):
    chat = models.IntegerField(verbose_name="идентификатор чата", default=0, unique=True)
    name = models.CharField(verbose_name="имя", max_length=40)
    target = models.TextField(verbose_name="цель")
    youtube = models.CharField(verbose_name="идентификатор youtube канала", max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True,
                                 verbose_name="категория")
    playlist_id = models.CharField(max_length=200, blank=True, verbose_name="плейлист youtube канала")
    is_username = models.BooleanField(default=False)
    rating = models.IntegerField(default=0, verbose_name="рейтинг")

    def __str__(self):
        return f'имя - {self.name},\nчат - {self.chat}'

    class Meta:
        ordering = ['rating']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Question(models.Model):
    question = models.CharField(verbose_name="Вопрос", max_length=200)
    answer = models.TextField(verbose_name="Ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Частый вопрос"
        verbose_name_plural = "Частые вопросы"


class Task(models.Model):
    task_name = models.CharField(verbose_name="Задание", max_length=200, unique=True)
    task_text = models.TextField(verbose_name="Текст задания")
    task_rating = models.IntegerField(verbose_name="Количество рейтинга за выполнение", default=2)
    datetime = models.DateField(verbose_name="Дата публикации вопроса", default=date.today)

    def __str__(self):
        return self.task_name

    class Meta:
        verbose_name = "Задание для пользователям"
        verbose_name_plural = "Задания для пользователя"


class CompleteTask(models.Model):
    class StatusTask(models.TextChoices):
        CHECK = 'CH', 'Задание на проверке'
        COMPLETE = 'CM', 'Задание выполнено'
        FAIL = 'FL', 'Задание провалено'

    answer = models.TextField(verbose_name="Ответ", )
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Задание", )
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Пользователь", )
    status = models.CharField(max_length=2, choices=StatusTask.choices, default=StatusTask.CHECK, verbose_name="Статус задания", )
    comment = models.TextField(default="", verbose_name="Ваш комментарий", null=True, blank=True)

    def __str__(self):
        return f'{self.task} {self.user}'

    class Meta:
        verbose_name = "Задание на проверку"
        verbose_name_plural = "Задания на проверку"

