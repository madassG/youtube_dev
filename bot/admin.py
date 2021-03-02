from django.contrib import admin
from .models import Category, User, Task, CompleteTask
# Register your models here.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Task)
admin.site.register(CompleteTask)
