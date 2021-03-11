from django.contrib import admin
from .models import Category, User, Task, CompleteTask, Question

admin.site.register(Category)
admin.site.register(Question)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat', 'youtube', 'category')
    list_filter = ('category', )
    search_fields = ('chat', 'name', 'youtube')
    empty_value_display = '...'


admin.site.register(Task)
admin.site.register(CompleteTask)
