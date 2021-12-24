from youtubedev.celery import app
from datetime import date
from bot import models
import telebot
import os
import time
from dotenv import load_dotenv
load_dotenv(verbose=True)


@app.task
def check_publish():
    tasks = models.Task.objects.all().filter(is_publish=False)
    today = date.today()
    for task in tasks:
        if task.datetime == today:
            task.is_publish = True
            bot = telebot.TeleBot(os.getenv('BOT_API'))
            users = models.User.objects.all()
            i = 0
            for user in users:
                try:
                    bot.send_message(user.chat, "У вас новое задание."
                                                f"Задание:{task.task_name}")
                    i += 1
                    if i % 20 == 0:
                        time.sleep(2)
                except Exception:
                    pass
