from django.contrib import admin
from users.models import Reward, Subscription, Client
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from config.settings import EMAIL_TEMPLATE

from .forms import ClientCreationForm, ClientChangeForm


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_filter = ('belonging', 'type')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('title', 'slug', 'desc', '')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    add_form = ClientCreationForm
    form = ClientChangeForm
    model = Client
    list_display = ('name',
                    'surname',
                    'phone',
                    'email',
                    'email_proved',
                    'telegram_chat',
                    'subscription',
                    'date_joined'
                    )
    fieldsets = (
        (None, {'fields': ('email', 'email_proved', 'password')}),
        ('Информация', {'fields': ('name',
                                   'surname',
                                   'age',
                                   'phone',
                                   'telegram_chat',
                                   'subscription',
                                   'date_joined',
                                   'last_check',
                                   'rewards')}),
        ('Полномочия', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('username', 'name', 'surname', 'phone', 'email', 'telegram_chat')

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = Client.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            if not obj.password:
                obj.password = Client.objects.make_random_password(length=16)
                html_message = render_to_string(EMAIL_TEMPLATE, {'user': {'username': obj.email,
                                                                          'password': obj.password}, })
                message = EmailMessage('Регистрация в YTPromote', html_message, "noreply@ytpromote.com", [obj.email])
                message.content_subtype = 'html'
                message.send()
            obj.set_password(obj.password)
        obj.save()
