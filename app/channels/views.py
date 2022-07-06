from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from django.template.response import TemplateResponse, HttpResponse
from django.shortcuts import redirect
from datetime import datetime
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from channels.analysis import analyse_channel, video_data

import csv


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
    user_dict = model_to_dict(user)
    user_dict['pk'] = user.pk
    user_dict['category'] = user.category
    user_dict['registration_date'] = datetime.strftime(user.registration_date, '%Y-%m-%d %H:%m')
    context = {
        **site.each_context(request),
        'title': 'Страница пользователя',
        'user': user_dict,
        'changes': analyse_channel(user.id),
        'videos': video_data(user.id),
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
    return redirect('/admin/bot/user/')
    return TemplateResponse(request, 'admin/ratings.html', context)


@staff_member_required
def export_users(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['chat', 'name', 'target', 'youtube', 'category', 'playlist_id', 'subs_day', 'subs_week',
                     'subs_month', 'subs_quarter', 'views_day', 'views_week', 'views_month', 'views_quarter', 'rating',
                     'registration_date'])
    for user in User.objects.all().values_list('chat', 'name', 'target', 'youtube', 'category', 'playlist_id', 'subs_day', 'subs_week',
                     'subs_month', 'subs_quarter', 'views_day', 'views_week', 'views_month', 'views_quarter', 'rating',
                     'registration_date'):
        writer.writerow(user)

    response['Content-Disposition'] = 'attachment; filename="users.csv'

    return response
