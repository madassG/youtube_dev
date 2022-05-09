from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('channels', views.channels, name='channels'),
    path('channel/<int:channel_id>', views.channel, name='channel'),
    path('channel/<int:channel_id>/delete', views.delete_channel, name='delete_channel'),
    path('channels/add', views.add_channel, name='add_channel')
]
