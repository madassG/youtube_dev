from django.contrib import admin
from channels.models import Channel, Video


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('owner', 'subscribers', 'total_views', 'videos_quantity', 'created_at')
    fields = ('owner', 'subscribers', 'total_views', 'videos_quantity')


admin.site.register(Video)

admin.site.index_title = 'Администрирование'
admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Добро пожаловать в Админ-панель!'
