from django.core.management.base import BaseCommand
from django.utils import timezone
from bot import models
from bot.bot import Bot, User, Task, CompleteTask, Question, CheckTask, FailTask, Statistic, PersonalInformation
import telebot


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        bot = telebot.TeleBot('1606504631:AAG7mt6794Kzra04ZLx4i1vZtKy_9kAD0rw')
        function = Bot(bot)

        @bot.message_handler(content_types=['text'])
        def reactions(message):
            user_bot = User(chat=message.from_user.id, bot=bot)
            if user_bot.is_exist():
                user = models.User.objects.get(chat=message.from_user.id)
                if message.text == "/start" and user.last_message != message.text:
                    function.cabinet(message)
                elif message.text == "мои задания" and user.last_message != message.text:
                    print(user.last_message)
                    Task(bot, user).get(message)
                elif message.text == "выполненные задания" and user.last_message != message.text:
                    CompleteTask(bot, user).get(message)
                elif message.text == "задания на проверке" and user.last_message != message.text:
                    CheckTask(bot, user).get(message)
                elif message.text == "проваленные задания" and user.last_message != message.text:
                    FailTask(bot, user).get(message)
                elif message.text == "статистика" and user.last_message != message.text:
                    Statistic(bot, user).get(message)
                elif message.text == "личная информация" and user.last_message != message.text:
                    PersonalInformation(bot, user).get(message)
                elif user.last_message != message.text:
                    function.cabinet(message)
                user.last_message = message.text
                user.save()
            else:
                if message.text == "/start":
                    function.cabinet(message)
                elif message.text == "частые вопросы":
                    question = Question(bot)
                    questions = models.Question.objects.all()
                    keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
                    for q in questions:
                        keyboard2.add(telebot.types.KeyboardButton(q.question))

                    keyboard2.add(telebot.types.KeyboardButton('выход'))
                    bot.send_message(message.from_user.id, "Выбери интересующий тебя вопрос", reply_markup=keyboard2)
                    bot.register_next_step_handler(message, question.get)
                elif message.text == "регистрация":
                    user = User(message.from_user.id, bot)
                    if user.is_exist():
                        bot.send_message(message.from_user.id, "Ты уже с нами")
                    else:
                        bot.send_message(message.from_user.id, "Введите имя",
                                         reply_markup=telebot.types.ReplyKeyboardRemove())
                        bot.register_next_step_handler(message, user.getName)

        bot.polling()
