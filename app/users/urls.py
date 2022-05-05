from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('channels', views.channels, name='channels'),
    path('channel/<int:channel_id>', views.channel, name='channel')
]
