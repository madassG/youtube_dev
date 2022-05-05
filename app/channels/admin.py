from django.contrib import admin
from channels.models import Channel, Video, Account


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('owner', 'subscribers', 'total_views', 'videos_quantity', 'created_at')
    fields = ('owner', 'subscribers', 'total_views', 'videos_quantity')
    search_fields = ('owner__name', 'owner__chat')
    list_filter = ('owner', )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'viewCount', 'likeCount', 'dislikeCount', 'commentsCount', 'published_at')
    search_fields = ('title', )
    list_filter = ('owner', )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'owner', 'youtube', 'category', 'subs_day', 'subs_week', 'subs_month',
        'subs_quarter', 'views_day', 'views_week', 'views_month', 'views_quarter'
    )
    list_filter = ('category',)
    search_fields = ('owner', 'name', 'youtube')
    empty_value_display = '...'


admin.site.index_title = 'Администрирование'
admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Добро пожаловать в Админ-панель!'
