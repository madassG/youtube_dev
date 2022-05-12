from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from channels.models import Account, Channel, Video
from channels.forms import ChannelForm
from channels.analysis import analyse_channel, video_data
from django.core.paginator import Paginator

from users.utils import add_notification, NotificationType


@login_required(login_url='login')
def home(request):
    current_user = request.user
    rewards = [*list(current_user.rewards.all())]
    for acc in current_user.accounts.all():
        if len(acc.rewards.all()):
            rewards.append(*list(acc.rewards.all()))

    if current_user.subscription:
        current_user.subscription.desc = current_user.subscription.desc.replace('\n', '<br>')

    accounts = current_user.accounts.all()

    current_user.data = {
        'subscribers': 0,
        'total_views': 0,
        'videos_quantity': 0,
    }

    for account in accounts:
        last_check = list(Channel.objects.filter(owner=account).order_by('-created_at'))
        if not last_check:
            continue
        current_user.data['subscribers'] += last_check[0].subscribers
        current_user.data['total_views'] += last_check[0].total_views
        current_user.data['videos_quantity'] += last_check[0].videos_quantity

    current_user.channels_count = len(current_user.accounts.all())

    return render(request, 'user/home.html', {'user': current_user, 'rewards': rewards})


@login_required(login_url='login')
def channels(request):
    current_user = request.user
    accounts = current_user.accounts.all()

    nots = request.session.get('notification', [])
    request.session['notification'] = []

    for account in accounts:
        last_check = list(Channel.objects.filter(owner=account).order_by('-created_at'))
        if not last_check:
            account.data = {
                'subscribers': 0,
                'total_views': 0,
                'videos_quantity': 0,
                'created_at': None
            }
            continue
        account.data = last_check[0]

    return render(request, 'user/channels.html', {'accounts': accounts,
                                                  'max_accs': current_user.subscription.max_channels,
                                                  'nots': nots
                                                  })


@login_required(login_url='login')
def channel(request, channel_id: int):
    ch = get_object_or_404(Account, pk=channel_id)
    current_user = request.user

    if ch.owner != current_user:
        return HttpResponseForbidden("Нет доступа")

    last_check = list(Channel.objects.filter(owner=ch).order_by('-created_at'))
    if not last_check:
        ch.data = {
            'subscribers': 0,
            'total_views': 0,
            'videos_quantity': 0,
            'created_at': None
        }
    else:
        ch.data = last_check[0]

    paginator = Paginator(video_data(ch.pk), 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/channel.html', {'channel': ch, 'changes': analyse_channel(ch.pk),
                                                 'videos': page_obj})


@login_required(login_url='login')
def delete_channel(request, channel_id: int):
    ch = get_object_or_404(Account, pk=channel_id)
    current_user = request.user

    if ch.owner != current_user:
        return HttpResponseForbidden("Нет доступа")

    if request.method == 'POST':
        add_notification(request, NotificationType.success, f'Канал с id {ch.youtube} успешно удалён')
        ch.delete()
        return redirect('channels')

    return render(request, 'user/delete.html', {'name': ch.name})


@login_required(login_url='login')
def add_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if not form.is_valid():
            return render(request, 'user/add_channel.html', {'form': form})

        channel_id = form.cleaned_data['channel_id']

        acc = Account.objects.filter(youtube=channel_id)
        if acc:
            form.add_error('channel_id', 'Данный канал уже зарегистрирован в сервисе.')
            return render(request, 'user/add_channel.html', {'form': form})

        current_user = request.user

        if len(current_user.accounts.all()) + 1 > current_user.subscription.max_channels:
            add_notification(request, NotificationType.error, f'Лимит каналов, которые вы можете добавить с подпиской вашего уровня - {current_user.subscription.max_channels}')
            return redirect('channels')
        acc = Account(owner=current_user, youtube=channel_id, purpose=form.cleaned_data['purpose'])
        acc.save()

        add_notification(request, NotificationType.success, f'Канал с ID {acc.youtube} успешно добавлен. При следующей проверке информация по нему обновится.')

        return redirect('channels')
    return render(request, 'user/add_channel.html')
