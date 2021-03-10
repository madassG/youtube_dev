from django.contrib import admin
from channels.models import Channel, Video

admin.site.register(Channel)
admin.site.register(Video)

admin.site.index_title = 'Администрирование'
admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Добро пожаловать в Админ-панель!'
