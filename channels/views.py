from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from django.template.response import TemplateResponse
from bot.models import User
from datetime import datetime
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from channels.analysis import analyse_channel


@staff_member_required
def users_page(request):
    if request.GET.get('search', ''):
        users = User.objects.filter(chat__icontains=request.GET['search'])
        users2 = User.objects.filter(name__icontains=request.GET['search'])
        users = users | users2
    else:
        users = User.objects.order_by('name').all()
    pages = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {
        **site.each_context(request),
        'title': 'Пользователи',
        'page': page_obj
    }

    request.current_app = site.name

    return TemplateResponse(request, site.index_template or 'admin/users.html', context)


@staff_member_required
def user_page(request, user_id):
    user = User.objects.filter(chat=user_id)[0]
    changes = analyse_channel(user.id)
    user_dict = model_to_dict(user)
    user_dict['category'] = user.category
    context = {
        **site.each_context(request),
        'title': 'Страница пользователя',
        'user': user_dict,
        'changes': changes,
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
