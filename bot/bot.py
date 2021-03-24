from bot import models
import logging
import telebot

logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')


class Bot:
    def __init__(self, bot, user=None):
        self.bot = bot
        self.user = user

    def cabinet(self, message):
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
        try:
            user = models.User.objects.get(chat=message.from_user.id)
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


class Registration:
    def __init__(self, chat_id, bot):
        self.chat_id = chat_id
        self.bot = bot
        self.name = ""
        self.category = ""
        self.target = ""
        self.youtube = ""
        self.function = Bot(bot)
        self.is_username = False

    def getName(self, message):
        self.name = message.text
        self.bot.send_message(message.from_user.id, f"Приветствую, {self.name}. Чего ты хочешь добиться с нами?")
        self.bot.register_next_step_handler(message, self.getTarget)

    def getTarget(self, message):
        self.target = message.text
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keys = models.Category.objects.all()
        for key in keys:
            keyboard1.add(telebot.types.KeyboardButton(key.name))
        self.bot.send_message(message.from_user.id, "Отлично! Теперь укажи категорию", reply_markup=keyboard1)
        self.bot.register_next_step_handler(message, self.getCategory)

    def getCategory(self, message):
        categories = models.Category.objects.all()
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
        category_user = models.Category.objects.get(name=self.category)
        user = models.User(name=self.name, category=category_user,
                    chat=self.chat_id, target=self.target,
                    youtube=self.youtube, is_username=self.is_username)
        user.save()


class User(Registration):

    def __init__(self, chat, bot, user=None):
        if user is not None:
            self.name = user.name
            self.category = user.category.name
            self.target = user.target
            self.youtube = user.youtube
        super(User, self).__init__(chat, bot)

    def is_exist(self):
        try:
            if models.User.objects.get(chat=self.chat_id):
                return True
        except Exception:
            return False


class Task(Bot):
    def get(self, message):
        tasks1 = models.Task.objects.all().filter(is_publish=True, user=None)[:10]
        tasks2 = models.Task.objects.all().filter(is_publish=True, user=self.user)[:10]
        tasks = tasks1 | tasks2
        error = False
        user = self.user
        if not error:
            keys = []
            self.bot.send_message(message.from_user.id, "Ваши задания:")
            for task in tasks:
                try:
                    if models.CompleteTask.objects.get(user=user, task=task):
                        continue
                except Exception:
                    print(task.user)
                    keys += [task.task_name]
                    self.bot.send_message(message.from_user.id, "-" * 30)
                    self.bot.send_message(message.from_user.id, f" Задание: {task.task_name} \n{task.task_text}")
            if not keys:
                self.bot.send_message(message.from_user.id, "Заданий пока нет")
                self.cabinet(message)
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
            self.cabinet(message)

    def put(self, message):
        if message.text == "выход":
            self.cabinet(message)
        else:
            try:
                task = models.Task.objects.get(task_name=message.text)
                completeTask = models.CompleteTask.objects.all().filter(task=task, user=self.user)
                for complete in completeTask:
                    complete.delete()
                print(completeTask)
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('отменить')
                self.task = models.Task.objects.get(task_name=message.text)
                self.bot.send_message(message.from_user.id, "Введите ответ или комментарий к вашей работе",
                                      reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.response)
            except Exception:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
                self.get(message)

    def response(self, message):
        user = self.user
        if message.text != "отменить":
            answer = message.text
            complete = models.CompleteTask(answer=answer, task=self.task, user=user)
            complete.save()
            self.bot.send_message(message.from_user.id, "Ответ сохранен")
        self.get(message)


class CompleteTask(Bot):
    def get(self, message):
        user = self.user
        is_exist = False
        try:
            completes = models.CompleteTask.objects.all().filter(user=user, status='CM')[:10]
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
        self.cabinet(message)


class CheckTask(Bot):
    def get(self, message):
        user = self.user
        is_exist = False
        try:
            completes = models.CompleteTask.objects.all().filter(user=user, status='CH')[:10]
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
        self.cabinet(message)


class FailTask(Bot):
    def get(self, message):
        user = self.user
        is_exist = False
        try:
            completes = models.CompleteTask.objects.all().filter(user=user, status='FL')
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
                self.cabinet(message)
        except Exception:
            self.bot.send_message(message.from_user.id, "Вы молодец! У вас нет проваленных заданий!")

    def put(self, message):
        if message.text == "выход":
            self.cabinet(message)
        else:
            user = self.user
            try:
                task = models.Task.objects.get(task_name=message.text)
                completeTask = models.CompleteTask.objects.all().filter(task=task, user=user)
                for complete in completeTask:
                    complete.delete()
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('отменить')
                self.task = models.Task.objects.get(task_name=message.text)
                self.bot.send_message(message.from_user.id, "Введите ответ или комментарий к вашей работе", reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.response)
            except Exception:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
                self.get(message)

    def response(self, message):
        user = self.user
        if message.text != "отменить":
            answer = message.text
            complete = models.CompleteTask(answer=answer, task=self.task, user=user)
            complete.save()
            self.bot.send_message(message.from_user.id, "Ответ сохранен")
        self.get(message)


class PersonalInformation(Bot):
    def get(self, message):
        user = self.user
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
        if message.text.lower() == "выход":
            self.cabinet(message)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.add(telebot.types.KeyboardButton('отменить'))
            if message.text == "Имя":
                self.bot.send_message(message.from_user.id, "Введите новое имя:", reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.rename)
            if message.text == "Цель":
                self.bot.send_message(message.from_user.id, "Введите новую цель:", reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.retarget)

    def rename(self, message):
        if message.text == "отменить":
            self.get(message)
        else:
            name = message.text
            user = self.user
            user.name = name
            user.save()
            self.bot.send_message(message.from_user.id, 'имя изменено')
            self.get(message)

    def retarget(self, message):
        if message.text == "отменить":
            self.get(message)
        else:
            target = message.text
            user = self.user
            user.target = target
            user.save()
            self.bot.send_message(message.from_user.id, 'имя изменено')
            self.get(message)


class Statistic(Bot):
    def get(self, message):
        user = self.user
        users = models.User.objects.all().filter(category=user.category).order_by('-rating')
        users_best = users[:2]
        level = 1
        user_exist_in_list = False
        for u in users_best:
            if u.chat == user.chat:
                self.bot.send_message(user.chat, f"место: {level}\nпользователь (это вы):{u.name}\nс рейтингом {u.rating}")
                user_exist_in_list = True
            else:
                self.bot.send_message(user.chat, f"место: {level}\nпользователь:{u.name}\nс рейтингом {u.rating}")
            level += 1
        if not user_exist_in_list:
            for u in users:
                if u.chat == user.chat:
                    self.bot.send_message(user.chat,
                                          f"место: {level}\nпользователь (это вы):{u.name}\nс рейтингом {u.rating}")
                    break
                level += 1


class Question(Bot):
    def get(self, message):
        if message.text == "выход":
            self.cabinet(message)
        else:
            try:
                question = models.Question.objects.get(question=message.text)
                self.bot.send_message(message.from_user.id, question.answer)
            except models.models.ObjectDoesNotExist:
                self.bot.send_message(message.from_user.id, "такого вопроса нет")
                self.cabinet(message)
            self.bot.register_next_step_handler(message, self.get)
