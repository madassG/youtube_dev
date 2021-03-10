from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from django.template.response import TemplateResponse


@staff_member_required
def users_page(request):

    context = {
        **site.each_context(request),
    }

    request.current_app = site.name

    return TemplateResponse(request, site.index_template or 'admin/users.html', context)


@staff_member_required
def user_page(request, user_id):
    context = {
        **site.each_context(request),
    }

    request.current_app = site.name
    return TemplateResponse(request, 'admin/user.html', context)


@staff_member_required
def ratings(request):
    context = {
        **site.each_context(request),
    }

    request.current_app = site.name
    return TemplateResponse(request, 'admin/ratings.html', context)
