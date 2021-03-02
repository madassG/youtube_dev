from django.core.management.base import BaseCommand
from django.utils import timezone
from bot.models import Category, User, Task, CompleteTask
import telebot


# class Registration:
#     pass


class Registration:

    def __init__(self, chat_id, bot):
        self.chat_id = chat_id
        self.bot = bot
        self.name = ""
        self.category = ""
        self.target = ""
        self.youtube = ""

    def getName(self, message):
        self.name = message.text
        self.bot.send_message(message.from_user.id, "Расскажите свою цель")
        self.bot.register_next_step_handler(message, self.getTarget)

    def getTarget(self, message):
        self.target = message.text
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keys = Category.objects.all()
        keys_name = []
        for key in keys:
            keys_name += [key.name]
        keyboard1.row(*keys_name)
        self.bot.send_message(message.from_user.id, "Укажите категорию", reply_markup=keyboard1)
        self.bot.register_next_step_handler(message, self.getCategory)

    def getCategory(self, message):
        self.category = message.text
        self.bot.send_message(message.from_user.id, "Укажите ссылку на ваш ютуб канал", reply_markup=None)
        self.bot.register_next_step_handler(message, self.getYoutube)

    def getYoutube(self, message):
        self.youtube = message.text
        self.createUser()
        self.bot.send_message(message.from_user.id, "Ты в банде!")

    def createUser(self):
        category_user = Category.objects.get(name=self.category)
        user = User(name=self.name, category=category_user, chat=self.chat_id, target=self.target, youtube=self.youtube)
        user.save()


class user_bot(Registration):

    def __init__(self, chat, bot, user=None):
        if user is not None:
            self.name = user.name
            self.category = user.category.name
            self.target = user.target
            self.youtube = user.youtube
        super(user_bot, self).__init__(chat, bot)

    def is_exist(self):
        try:
            if User.objects.get(chat=self.chat_id):
                return True
        except Exception:
            return False

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
                user = user_bot(message.from_user.id, bot)
                if user.is_exist():
                    bot.send_message(message.from_user.id, "Ты уже с нами")
                else:
                    bot.send_message(message.from_user.id, "Введите имя")
                    bot.register_next_step_handler(message, user.getName)


        def questions(message):
            answers = {
                'вопрос 1': "ответ 1",
                'вопрос 2': "ответ 2",
                "вопрос 3": "ответ 3"
            }

            if message.text == "выход":
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

        bot.polling()
