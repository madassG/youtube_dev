from django.core.management.base import BaseCommand
from django.utils import timezone
from bot.models import Category, User, Task, CompleteTask, Question
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
        self.is_username = False

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
        is_correct = False
        is_id = False
        if message.text.startswith("https://www.youtube.com/c/") or message.text.startswith("https://youtube.com/c/"):
            is_correct = True
            is_id = True
            self.is_username = True
        elif message.text.startswith("https://www.youtube.com/channel") or message.text.startswith("https://youtube.com/channel"):
            is_correct = True

        if is_id:
            self.bot.send_message(message.from_user.id, "Пожалуйста укажите ссылку с id канала. Пример:\n"
                                                        "https://www.youtube.com/channel/ваш_айди")
            self.bot.register_next_step_handler(message, self.getYoutube)
        elif is_correct:
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
        user = User(name=self.name, category=category_user,
                    chat=self.chat_id, target=self.target,
                    youtube=self.youtube, is_username=self.is_username)
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


class my_task:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(bot)

    def get(self, message):
        tasks = Task.objects.all()
        error = False
        user = None
        try:
            user = User.objects.get(chat=message.from_user.id)
        except Exception:
            error = True
        if not error:
            keys = []
            self.bot.send_message(message.from_user.id, "Ваши задания:")
            for task in tasks:
                try:
                    if CompleteTask.objects.get(user=user, task=task):
                        continue
                except Exception:
                    keys += [task.task_name]
                    self.bot.send_message(message.from_user.id, "-" * 30)
                    self.bot.send_message(message.from_user.id, f" Задание: {task.task_name} \n{task.task_text}")
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
                self.bot.register_next_step_handler(message, self.put)
        else:
            self.bot.send_message(message.from_user.id, "ой-ей, кажется ошибка.")
            self.function.cabinet(message)

    def put(self, message):
        if message.text == "выход":
            self.function.cabinet(message)
        else:
            try:
                user = User.objects.get(chat=message.from_user.id)
                task = Task.objects.get(task_name=message.text)
                completeTask = CompleteTask.objects.all().filter(task=task, user=user)
                for complete in completeTask:
                    complete.delete()
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('отменить')
                self.task = Task.objects.get(task_name=message.text)
                self.bot.send_message(message.from_user.id, "Введите ответ или комментарий к вашей работе", reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.response)
            except Exception:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
                self.get(message)

    def response(self, message):
        user = User.objects.get(chat=message.from_user.id)
        if message.text != "отменить":
            answer = message.text
            complete = CompleteTask(answer=answer, task=self.task, user=user)
            complete.save()
            self.bot.send_message(message.from_user.id, "Ответ сохранен")
        self.get(message)


class complete_task:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(bot)
    def get(self, message):
        user = User.objects.get(chat=message.from_user.id)
        is_exist = False
        try:
            completes = CompleteTask.objects.all().filter(user=user, status='CM')
            for complete in completes:
                comment = ""
                if complete.comment != "":
                    comment = f"\nКомментарий создателя:" + f"\n{complete.comment}"
                self.bot.send_message(message.from_user.id, f" Задание:"
                                                            f"\n{complete.task.task_name}"
                                                            f"\nТекст Задания:"
                                                            f"\n{complete.task.task_text}"
                                                            f"\nВаш ответ:"
                                                            f"\n{complete.answer}" + comment)
                is_exist = True
        except Exception:
            self.bot.send_message(message.from_user.id, "Вы еще не выполнили ни одного задания")
        if not is_exist:
            self.bot.send_message(message.from_user.id, "Вы еще не выполнили ни одного задания")
        self.function.cabinet(message)


class check_task:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(bot)

    def get(self, message):
        user = User.objects.get(chat=message.from_user.id)
        is_exist = False
        try:
            completes = CompleteTask.objects.all().filter(user=user, status='CH')
            for complete in completes:
                self.bot.send_message(message.from_user.id, f" Задание:"
                                                            f"\n{complete.task.task_name}"
                                                            f"\nТекст Задания:"
                                                            f"\n{complete.task.task_text}"
                                                            f"\nВаш ответ:"
                                                            f"\n{complete.answer}")
                is_exist = True
        except Exception:
            self.bot.send_message(message.from_user.id, "Вы еще не выполнили ни одного задания")
        if not is_exist:
            self.bot.send_message(message.from_user.id, "Вы еще не выполнили ни одного задания")
        self.function.cabinet(message)


class fail_task:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(bot)

    def get(self, message):
        user = User.objects.get(chat=message.from_user.id)
        is_exist = False
        try:
            completes = CompleteTask.objects.all().filter(user=user, status='FL')
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            for complete in completes:
                keyboard.add(telebot.types.KeyboardButton(complete.task.task_name))
                comment = ""
                if complete.comment != "":
                    comment = f"\nКомментарий создателя:" + f"\n{complete.comment}"
                self.bot.send_message(message.from_user.id, f" Задание:"
                                                            f"\n{complete.task.task_name}"
                                                            f"\nТекст Задания:"
                                                            f"\n{complete.task.task_text}"
                                                            f"\nВаш ответ:"
                                                            f"\n{complete.answer}" + comment)
                is_exist = True
            if is_exist:
                keyboard.add(telebot.types.KeyboardButton('выход'))
                self.bot.send_message(message.from_user.id, "Выберите задание, которое хотите исправить",
                                      reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.put)
            else:
                self.bot.send_message(message.from_user.id, "Вы молодец! У вас нет проваленных заданий!")
                self.function.cabinet(message)
        except Exception:
            self.bot.send_message(message.from_user.id, "Вы молодец! У вас нет проваленных заданий!")

    def put(self, message):
        if message.text == "выход":
            self.function.cabinet(message)
        else:
            user = User.objects.get(chat=message.from_user.id)
            try:
                task = Task.objects.get(task_name=message.text)
                completeTask = CompleteTask.objects.all().filter(task=task, user=user)
                for complete in completeTask:
                    complete.delete()
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('отменить')
                self.task = Task.objects.get(task_name=message.text)
                self.bot.send_message(message.from_user.id, "Введите ответ или комментарий к вашей работе", reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.response)
            except Exception:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
                self.get(message)

    def response(self, message):
        user = User.objects.get(chat=message.from_user.id)
        if message.text != "отменить":
            answer = message.text
            complete = CompleteTask(answer=answer, task=self.task, user=user)
            complete.save()
            self.bot.send_message(message.from_user.id, "Ответ сохранен")
        self.get(message)


class personal_information:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(bot)

    def get(self, message):
        user = User.objects.get(chat=message.from_user.id)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keys = ['Имя', 'Цель', 'Выход']
        for key in keys:
            keyboard.add(telebot.types.KeyboardButton(key))
        self.bot.send_message(user.chat, f'Ваше имя: {user.name}')
        self.bot.send_message(user.chat, f'Ваша цель: {user.target}')
        self.bot.send_message(user.chat, f'Ваша категория: {user.category}')
        self.bot.send_message(user.chat, "Введите, что хотите изменить", reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.put)

    def put(self, message):
        if message.text == "выход":
            self.function.cabinet(message)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.add(telebot.types.KeyboardButton('отменить'))
            if message.text == "Имя":
                self.bot.send_message(message.from_user.id, "Введите новое имя:", reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.rename)
            if message.text == "Цель":
                self.bot.send_message(message.from_user.id, "Введите новую цель:", reply_markup=keyboard)

    def rename(self, message):
        if message.text == "отменить":
            self.get(message)
        else:
            name = message.text
            user = User.objects.get(chat=message.from_user.id)
            user.name = name
            user.save()
            self.bot.send_message(message.from_user.id, 'имя изменено')
            self.get(message)

    def retarget(self, message):
        if message.text == "отменить":
            self.get(message)
        else:
            target = message.text
            user = User.objects.get(chat=message.from_user.id)
            user.target = target
            user.save()
            self.bot.send_message(message.from_user.id, 'имя изменено')
            self.get(message)


class statistic_bot:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(bot)

    def get(self, message):
        user = User.objects.get(chat=message.from_user.id)
        users = User.objects.all().filter(category=user.category).order_by('-rating')[:2]
        level = 1
        user_exist_in_list = False
        for u in users:
            if u.chat == user.chat:
                self.bot.send_message(user.chat, f"место: {level}\nпользователь (это вы):{u.name}\nс рейтингом {u.rating}")
                user_exist_in_list = True
            else:
                self.bot.send_message(user.chat, f"место: {level}\nпользователь:{u.name}\nс рейтингом {u.rating}")
            level += 1
        users = User.objects.all().filter(category=user.category).order_by('-rating')
        if not user_exist_in_list:
            for u in users:
                if u.chat == user.chat:
                    self.bot.send_message(user.chat,
                                          f"место: {level}\nпользователь (это вы):{u.name}\nс рейтингом {u.rating}")
                    break
                level += 1


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
            keys = [
                'мои задания', 'выполненные задания', 'проваленные задания',
                'задания на проверке', 'статистика', 'личная информация'
            ]
            for key in keys:
                keyboard1.add(telebot.types.KeyboardButton(key))
            self.bot.send_message(message.from_user.id, "Выберите подходящий пункт", reply_markup=keyboard1)

        keyboard1.row(*keys)


class question_bot:
    def __init__(self, bot):
        self.bot = bot
        self.function = Function(bot)

    def get(self, message):
        if message.text == "выход":
            self.function.cabinet(message)
        else:
            try:
                question = Question.objects.get(question=message.text)
                self.bot.send_message(message.from_user.id, question.answer)
            except Exception:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
            self.bot.register_next_step_handler(message, self.get)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        bot = telebot.TeleBot('1656884535:AAHCagwHxEMRPUrg3UjuJpOqMbI1Ezosxo0')
        function = Function(bot)

        @bot.message_handler(content_types=['text'])
        def reactions(message):
            user = user_bot(chat=message.from_user.id, bot=bot)

            if user.is_exist():
                if message.text == "/start":
                    function.cabinet(message)
                elif message.text == "мои задания":
                    my_task(bot).get(message)
                elif message.text == "выполненные задания":
                    complete_task(bot).get(message)
                elif message.text == "задания на проверке":
                    check_task(bot).get(message)
                elif message.text == "проваленные задания":
                    fail_task(bot).get(message)
                elif message.text == "статистика":
                    statistic_bot(bot).get(message)
                elif message.text == "личная информация":
                    personal_information(bot).get(message)
                else:
                    function.cabinet(message)
            else:
                if message.text == "/start":
                    function.cabinet(message)
                elif message.text == "частые вопросы":
                    question = question_bot(bot)
                    questions = Question.objects.all()
                    keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
                    for q in questions:
                        keyboard2.add(telebot.types.KeyboardButton(q.question))

                    keyboard2.add(telebot.types.KeyboardButton('выход'))
                    bot.send_message(message.from_user.id, "Выбери интересующий тебя вопрос", reply_markup=keyboard2)
                    bot.register_next_step_handler(message, question.get)
                elif message.text == "регистрация":
                    user = user_bot(message.from_user.id, bot)
                    if user.is_exist():
                        bot.send_message(message.from_user.id, "Ты уже с нами")
                    else:
                        bot.send_message(message.from_user.id, "Введите имя",
                                         reply_markup=telebot.types.ReplyKeyboardRemove())
                        bot.register_next_step_handler(message, user.getName)

        bot.polling()
