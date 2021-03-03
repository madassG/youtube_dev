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
        self.function = Function(bot)

    def getName(self, message):
        self.name = message.text
        self.bot.send_message(message.from_user.id, f"Приветствую, {self.name}. Чего ты хочешь добиться с нами?")
        self.bot.register_next_step_handler(message, self.getTarget)

    def getTarget(self, message):
        self.target = message.text
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keys = Category.objects.all()
        for key in keys:
            keyboard1.add(telebot.types.KeyboardButton(key.name))
        self.bot.send_message(message.from_user.id, "Отлично! Теперь укажи категорию", reply_markup=keyboard1)
        self.bot.register_next_step_handler(message, self.getCategory)

    def getCategory(self, message):
        categories = Category.objects.all()
        for category in categories:
            if category.name == message.text:
                self.category = message.text
                self.bot.send_message(message.from_user.id, "Прекрасный выбор."
                                                            " Далее нужно указать ссылку на ваш ютуб канал"
                                                            "(будьте бдительны, изменить ее нельзя)",
                                      reply_markup=telebot.types.ReplyKeyboardRemove())
                self.bot.register_next_step_handler(message, self.getYoutube)
                break
        else:
            keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
            keys_name = []
            for key in categories:
                keyboard1.add(telebot.types.KeyboardButton(key.name))
            self.bot.send_message(message.from_user.id, "Такой категории нет. Пожалуйста, повторите попытку!", reply_markup=keyboard1)
            self.bot.register_next_step_handler(message, self.getCategory)

    def getYoutube(self, message):
        if message.text.startswith("https://www.youtube.com/c") or \
           message.text.startswith("https://www.youtube.com/channel") or \
           message.text.startswith("https://youtube.com/channel") or \
           message.text.startswith("https://youtube.com/c"):
            youtubes = message.text.split('/')
            if youtubes[4] == "":
                self.bot.send_message(message.from_user.id, "Это не ссылка на ютуб канал. Повторите попытку!")
                self.bot.register_next_step_handler(message, self.getYoutube)
            else:
                self.youtube = youtubes[4]
                self.createUser()
                self.bot.send_message(message.from_user.id, "Поздравляю, теперь вы станете популярным!!")
                self.function.cabinet(message)
        else:
            self.bot.send_message(message.from_user.id, "Это не ссылка на ютуб канал. Повторите попытку!")
            self.bot.register_next_step_handler(message, self.getYoutube)

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


class Task_bot:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(self.bot)
        self.Task = ""

    def put_task(self, message):
        if message.text == "выход":
            self.function.cabinet(message)
        else:
            try:
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('отменить')
                self.task = Task.objects.get(task_name=message.text)
                self.bot.send_message(message.from_user.id, "Введите ответ", reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.response_task)
            except Exception:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
                self.bot.register_next_step_handler(message, self.all_task)

    def response_task(self, message):
        user = User.objects.get(chat=message.from_user.id)
        if message.text != "отменить":
            answer = message.text
            complete = CompleteTask(answer=answer, task=self.task, user=user)
            complete.save()
            self.bot.send_message(message.from_user.id, "Ответ сохранен")
        self.all_task(message)

    def all_task(self, message):
        tasks = Task.objects.all()
        error = False
        try:
            user_it = User.objects.get(chat=message.from_user.id)
        except:
            error = True
        if not error:
            keys = []
            self.bot.send_message(message.from_user.id, "Ваши задания:")
            for task_it in tasks:
                try:
                    if CompleteTask.objects.get(task=task_it, user=user_it):
                        continue
                except Exception:
                    keys += [task_it.task_name]
                    self.bot.send_message(message.from_user.id, "-" * 30)
                    self.bot.send_message(message.from_user.id, f" Задание: {task_it.task_name} \n{task_it.task_text}")
            if not keys:
                self.bot.send_message(message.from_user.id, "Заданий пока нет")
                self.function.cabinet(message)
            else:
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                for key in keys:
                    keyboard.add(telebot.types.KeyboardButton(key))
                keyboard.add('выход')
                self.bot.send_message(message.from_user.id, "Выберите задание, которое хотите сделать",
                                      reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.put_task)
        else:
            self.bot.send_message(message.from_user.id, "ой-ей, кажется ошибка.")
            self.function.cabinet(message)

    def complete_task(self, message):
        try:
            user = User.objects.get(chat=message.from_user.id)
            completes = CompleteTask.objects.all().filter(user=user)
            for complete in completes:
                self.bot.send_message(message.from_user.id, f" Задание:"
                                                            f"\n{complete.task.task_name}"
                                                            f"\nТекст Задания:"
                                                            f"\n{complete.task.task_text}"
                                                            f"\nВаш ответ:"
                                                            f"\n{complete.answer}")
            else:
                self.bot.send_message(message.from_user.id, "Вы еще не выполнили ни одного задания")
        except:
            self.bot.send_message(message.from_user.id, "Вы еще не выполнили ни одного задания")


class Function:
    def __init__(self, bot):
        self.bot = bot
        self.Task = ""

    def cabinet(self, message):
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
        try:
            user = User.objects.get(chat=message.from_user.id)
        except Exception:
            user = None
        if user is None:
            keys = [
                'регистрация', 'частые вопросы',
            ]
            for key in keys:
                keyboard1.add(telebot.types.KeyboardButton(key))
            if message.text == "/start":
                self.bot.send_message(message.from_user.id, "Приветствую тебя! Я Данила научу тебя быть видеоблогером, "
                                                            "выбери подходящий тебе пункт", reply_markup=keyboard1)
            else:
                self.bot.send_message(message.from_user.id, "Выберите подходящий пункт", reply_markup=keyboard1)
        else:
            keys = {
                'мои задания', 'выполненные задания', 'статистика'
            }
            for key in keys:
                keyboard1.add(telebot.types.KeyboardButton(key))
            self.bot.send_message(message.from_user.id, "Выберите подходящий пункт", reply_markup=keyboard1)

        keyboard1.row(*keys)

    def questions(self, message):
        answers = {
            'вопрос 1': "ответ 1",
            'вопрос 2': "ответ 2",
            "вопрос 3": "ответ 3"
        }

        if message.text == "выход":
            self.cabinet(message)
        else:
            answer = message.text
            try:
                self.bot.send_message(message.from_user.id, answers[answer])
            except KeyError:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
            self.bot.register_next_step_handler(message, self.questions)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        bot = telebot.TeleBot('1656884535:AAHCagwHxEMRPUrg3UjuJpOqMbI1Ezosxo0')
        function = Function(bot)

        @bot.message_handler(content_types=['text'])
        def reactions(message):
            if message.text == "/start":
                function.cabinet(message)
            elif message.text == "частые вопросы":
                keys = [
                    "вопрос 1", "вопрос 2", "вопрос 3", 'выход'
                ]

                keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
                keyboard2.row(*keys)
                bot.send_message(message.from_user.id, "Выбери интересующий тебя вопрос", reply_markup=keyboard2)
                bot.register_next_step_handler(message, function.questions)
            elif message.text == "регистрация":
                user = user_bot(message.from_user.id, bot)
                if user.is_exist():
                    bot.send_message(message.from_user.id, "Ты уже с нами")
                else:
                    bot.send_message(message.from_user.id, "Введите имя",
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(message, user.getName)
            elif message.text == "мои задания":
                Task_bot(bot).all_task(message)
            elif message.text == "выполненные задания":
                Task_bot(bot).complete_task(message)
            elif message.text == "статистика":
                bot.send_message(message.from_user.id, "функция в разработке. А пока выполняйте задания!")
            else:
                bot.send_message(message.from_user.id, "Извините, произошла ошибка")
                function.cabinet(message)

        bot.polling()
