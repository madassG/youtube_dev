from django.db import models
from datetime import datetime
from datetime import date
import telebot
import os
from dotenv import load_dotenv
import time
load_dotenv(verbose=True)

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
    last_message = models.TextField(default="")
    registration_date = models.DateTimeField(auto_now_add=True)

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
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.datetime == date.today() and not self.is_publish:
            self.is_publish = True
            bot = telebot.TeleBot(os.getenv('YT_API'))
            users = User.objects.all()
            i = 0
            for user in users:
                try:
                    bot.send_message(user.chat, "У вас новое задание."
                                                f"Задание:{self.task_name}")
                    i += 1
                    if i % 20 == 0:
                        time.sleep(2)
                except Exception:
                    pass
        super(Task, self).save(*args, **kwargs)

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
    okey = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task} {self.user}'

    def save(self, *args, **kwargs):
        if self.status == 'CM' and not self.okey:
            self.user.rating += self.task.task_rating
            self.user.save()
            bot = telebot.TeleBot(os.getenv('YT_API'))
            bot.send_message(self.user.chat, "Вы выполнили задание!"
                                             f"\nЗадание:{self.task.task_name}"
                                             f"\n{self.comment}")
            self.okey = True
        if self.status == 'FL':
            bot = telebot.TeleBot(os.getenv('YT_API'))
            bot.send_message(self.user.chat, "Вы провалили задание!"
                                             f"\nЗадание:{self.task.task_name}"
                                             f"\n{self.comment}")

        super(CompleteTask, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Задание на проверку"
        verbose_name_plural = "Задания на проверку"


class UserTime(models.Model):
    chat = models.IntegerField(unique=True, default=0)
    time_from_last_message = models.TimeField(default=datetime.now(tz=None))
