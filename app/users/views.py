from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from channels.models import Account, Channel, Video
from channels.forms import ChannelForm
from channels.analysis import analyse_channel, video_data
from django.core.paginator import Paginator


@login_required(login_url='login')
def home(request):
    current_user = request.user
    rewards = [*list(current_user.rewards.all())]
    for acc in current_user.accounts.all():
        rewards.append(*list(acc.rewards.all()))

    if current_user.subscription:
        current_user.subscription.desc = current_user.subscription.desc.replace('\n', '<br>')

    return render(request, 'user/home.html', {'user': current_user, 'rewards': rewards})


@login_required(login_url='login')
def channels(request):
    current_user = request.user
    accounts = current_user.accounts.all()

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
                                                  'max_accs': current_user.subscription.max_channels
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
        acc = Account(owner=current_user, youtube=channel_id, purpose=form.cleaned_data['purpose'])
        acc.save()

        return redirect('channels')
    return render(request, 'user/add_channel.html')
