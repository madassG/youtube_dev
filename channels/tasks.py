from youtubedev.celery import app
from bot.models import User
from channels.models import Channel
from channels.channel import check_channel


def tmp_parcer(url):
    result = 'NO'
    if url.find('channel/') != -1:
        id_start = url.find('channel/') + 8
        result = url[id_start:]
    return result


@app.task
def check_accounts():
    Users = User.objects.all()
    for user in Users:
        channel_id = tmp_parcer(user.youtube)
        if channel_id != 'NO':
            data = check_channel(channel_id)
            new_data = Channel()
            new_data.owner = user
            new_data.subscribers = data['subscriberCount']
            new_data.total_views = data['viewCount']
            new_data.videos_quantity = data['videoCount']
            new_data.save()


@app.task
def check_videos():
    pass
