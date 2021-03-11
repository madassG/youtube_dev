from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from django.template.response import TemplateResponse
from bot.models import User

@staff_member_required
def users_page(request):

    context = {
        **site.each_context(request),
        'title': 'Пользователи'
    }

    request.current_app = site.name

    return TemplateResponse(request, site.index_template or 'admin/users.html', context)


@staff_member_required
def user_page(request, user_id):
    user = User.objects.filter(chat='752378415')[0]
    channel_checks = user.channels.all().order_by('created_at')

    views, subs, quantity, created_at = [], [], [], []
    for check in list(channel_checks):
        subs.append(check.subscribers)
        views.append(check.total_views)
        quantity.append(check.videos_quantity)
        created_at.append(check.created_at)
    data = {
        'views': views,
        'subs': subs,
        'quantity': quantity,
        'date': created_at,
    }
    context = {
        **site.each_context(request),
        'title': 'Страница пользователя',
        'data': data
    }

    request.current_app = site.name
    return TemplateResponse(request, 'admin/user.html', context)


@staff_member_required
def ratings(request):
    context = {
        **site.each_context(request),
        'title': 'Рейтинги'
    }

    request.current_app = site.name
    return TemplateResponse(request, 'admin/ratings.html', context)
