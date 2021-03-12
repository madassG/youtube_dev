from youtubedev.celery import app
from datetime import date
from bot import models
import telebot

@app.task
def check_publish():
    tasks = models.Task.objects.all().filter(is_publish=False)
    today = date.today()
    for task in tasks:
        if task.datetime == today:
            task.is_publish = True
            bot = telebot.TeleBot('1656884535:AAHCagwHxEMRPUrg3UjuJpOqMbI1Ezosxo0')
            users = models.User.objects.all()
            for user in users:
                try:
                    bot.send_message(user.chat, "У вас новое задание."
                                                f"Задание:{task.task_name}")
                except Exception:
                    pass
