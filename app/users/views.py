from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from channels.models import Account


@login_required(login_url='login')
def home(request):
    current_user = request.user
    rewards = [*list(current_user.rewards.all())]
    for acc in current_user.accounts.all():
        rewards.append(*list(acc.rewards.all()))

    current_user.subscription.desc = current_user.subscription.desc.replace('\n', '<br>')

    return render(request, 'user/home.html', {'user': current_user, 'rewards': rewards})


@login_required(login_url='login')
def channels(request):
    return render(request, 'user/channels.html')


@login_required(login_url='login')
def channel(request, channel_id: int):
    ch = get_object_or_404(Account, pk=channel_id)
    current_user = request.user

    if ch.owner != current_user:
        return HttpResponseForbidden("Нет доступа")
    return render(request, 'user/channel.html', {'channel': ch})
