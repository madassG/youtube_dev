from django.contrib import admin
from .models import Category, User, Task, CompleteTask, Question

admin.site.register(Category)
admin.site.register(Question)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat', 'youtube', 'category', 'registration_date')
    list_filter = ('category',)
    search_fields = ('chat', 'name', 'youtube')
    empty_value_display = '...'
    fields = ('name', 'youtube', 'target', 'category', 'rating')

    def has_add_permission(self, request):
        return False


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_rating', 'datetime')
    search_fields = ('task_name', )
    list_filter = ('datetime', )
    fields = ('task_name', 'task_text', 'task_rating', 'datetime', 'is_publish')


@admin.register(CompleteTask)
class CompleteTask(admin.ModelAdmin):
    list_display = ('task', 'user', 'answer', 'status', 'comment', )
    readonly_fields = ('user', 'task')
    list_filter = ('status', )

    def get_changeform_initial_data(self, request):
        print(1)
        return {'status': 'CH'}

    def has_add_permission(self, request):
        return False


