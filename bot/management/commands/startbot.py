from django.core.management.base import BaseCommand
from django.utils import timezone
from bot.models import Category, User
import telebot


# class Registration:
#     pass

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        bot = telebot.TeleBot('1656884535:AAHCagwHxEMRPUrg3UjuJpOqMbI1Ezosxo0')
        @bot.message_handler(content_types=['text'])
        def reactions(message):
            if message.text == "/start":
                keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
                keys = {
                    'регистрация', 'частые вопросы'
                }
                keyboard1.row(*keys)
                bot.send_message(message.from_user.id, "Приветствую тебя! Я Данила научу тебя быть видеоблогером, "
                                                       "выбери подходящий тебе пункт", reply_markup=keyboard1)
            elif message.text == "частые вопросы":
                keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
                keys = {
                    "вопрос 1", "вопрос 2", "вопрос 3", 'выход'
                }
                keyboard2.row(*keys)
                bot.send_message(message.from_user.id, "Выбери интересующий тебя вопрос", reply_markup=keyboard2)
                bot.register_next_step_handler(message, questions)
            elif message.text == "регистрация":
                user = User.objects.get(chat=message.from_user.id)
                if user is None:
                    user = User(chat=message.from_user.id, name="", target="", youtube="")
                    user.save()
                    bot.send_message(message.from_user.id, "Введите имя")
                    bot.register_next_step_handler(message, getname)
                else:
                    bot.send_message(message.from_user.id, "Вы уже с нами!")

        def questions(message):
            answers = {
                'вопрос 1': "ответ 1",
                'вопрос 2': "ответ 2",
                "вопрос 3": "ответ 3"
            }

            if( message.text == "выход" ):
                keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
                keyboard1.row('регистрация', 'частые вопросы')
                bot.send_message(message.from_user.id, "выберите интересующий вас пункт", reply_markup=keyboard1)
            else:
                answer = message.text
                try:
                    bot.send_message(message.from_user.id, answers[answer])
                except KeyError:
                    bot.send_message(message.from_user.id, "такого вопроса нет")
                bot.register_next_step_handler(message, questions)

        def getname(message):
            user = User.objects.get(chat=message.from_user.id)
            user.name = message.text
            user.save()
            bot.send_message(message.from_user.id, "Расскажите свою цель")
            bot.register_next_step_handler(message, getarget)

        def getarget(message):
            user = User.objects.get(chat=message.from_user.id)
            user.target = message.text
            user.save()
            bot.send_message(message.from_user.id, "Укажите ссылку на ваш ютуб канал")
            bot.register_next_step_handler(message, getyoutube)

        def getyoutube(message):
            user = User.objects.get(chat=message.from_user.id)
            user.youtube = message.text
            user.save()

        bot.polling()
